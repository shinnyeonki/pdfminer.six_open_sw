import os
import os.path
import struct
from io import BytesIO
from typing import BinaryIO, Tuple

try:
    from typing import Literal
except ImportError:
    # Literal was introduced in Python 3.8
    from typing_extensions import Literal  # type: ignore[misc]

from .jbig2 import JBIG2StreamReader, JBIG2StreamWriter
from .layout import LTImage
from .pdfcolor import LITERAL_DEVICE_CMYK
from .pdfcolor import LITERAL_DEVICE_GRAY
from .pdfcolor import LITERAL_DEVICE_RGB
from .pdftypes import (
    LITERALS_DCT_DECODE,
    LITERALS_JBIG2_DECODE,
    LITERALS_JPX_DECODE,
    LITERALS_FLATE_DECODE,
)

PIL_ERROR_MESSAGE = (
    "Could not import Pillow. This dependency of pdfminer.six is not "
    "installed by default. You need it to to save jpg images to a file. Install it "
    "with `pip install 'pdfminer.six[image]'`"
)


def align32(x: int) -> int:
    return ((x + 3) // 4) * 4


class BMPWriter:
    def __init__(self, fp: BinaryIO, bits: int, width: int, height: int) -> None:
        # BMP 파일을 생성하기 위한 초기 설정
        self.fp = fp  # 파일 포인터
        self.bits = bits  # 비트 수
        self.width = width  # 이미지의 너비
        self.height = height  # 이미지의 높이
        
        # 비트 수에 따른 컬러 테이블 크기 설정
        if bits == 1:
            ncols = 2  # 흑백
        elif bits == 8:
            ncols = 256  # 회색조
        elif bits == 24:
            ncols = 0  # 풀 컬러
        else:
            raise ValueError(bits)  # 1, 8, 24 외의 값은 오류
        
        # 한 줄당 데이터 크기 계산 (4바이트 경계로 정렬)
        self.linesize = align32((self.width * self.bits + 7) // 8)
        
        # 전체 데이터 크기 계산
        self.datasize = self.linesize * self.height
        
        # 헤더 크기 계산 (14: BMP 헤더, 40: DIB 헤더, ncols * 4: 컬러 테이블)
        headersize = 14 + 40 + ncols * 4
        
        # DIB 헤더 생성
        info = struct.pack(
            "<IiiHHIIIIII",
            40,
            self.width,
            self.height,
            1,
            self.bits,
            0,
            self.datasize,
            0,
            0,
            ncols,
            0,
        )
        assert len(info) == 40, str(len(info))  # DIB 헤더의 크기는 40바이트여야 함
        
        # BMP 헤더 생성
        header = struct.pack(
            "<ccIHHI", b"B", b"M", headersize + self.datasize, 0, 0, headersize
        )
        assert len(header) == 14, str(len(header))  # BMP 헤더의 크기는 14바이트여야 함
        
        # 헤더와 DIB 헤더를 파일에 쓰기
        self.fp.write(header)
        self.fp.write(info)
        
        # 컬러 테이블 생성 및 파일에 쓰기
        if ncols == 2:
            # 흑백 컬러 테이블
            for i in (0, 255):
                self.fp.write(struct.pack("BBBx", i, i, i))
        elif ncols == 256:
            # 회색조 컬러 테이블
            for i in range(256):
                self.fp.write(struct.pack("BBBx", i, i, i))
        
        # 데이터의 시작 위치와 종료 위치 계산
        self.pos0 = self.fp.tell()
        self.pos1 = self.pos0 + self.datasize

    def write_line(self, y: int, data: bytes) -> None:
        # 지정된 위치에 데이터 쓰기 (BMP는 이미지 데이터를 아래에서 위로 쓴다)
        self.fp.seek(self.pos1 - (y + 1) * self.linesize)
        self.fp.write(data)


class ImageWriter:
    """Write image to a file

    Supports various image types: JPEG, JBIG2 and bitmaps
    """

    def __init__(self, outdir: str) -> None:
        # 출력 디렉토리 설정
        self.outdir = outdir
        # 출력 디렉토리가 존재하지 않으면 생성
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def export_image(self, image: LTImage) -> str:
        """Save an LTImage to disk"""
        
        # 이미지의 너비와 높이를 가져옴
        (width, height) = image.srcsize

        # 이미지의 필터(압축 방식)를 가져옴
        filters = image.stream.get_filters()

        # 필터가 하나이고, 그 필터가 DCT 디코딩을 사용하는 경우 JPEG으로 저장
        if len(filters) == 1 and filters[0][0] in LITERALS_DCT_DECODE:
            name = self._save_jpeg(image)

        # 필터가 하나이고, 그 필터가 JPX 디코딩을 사용하는 경우 JPEG 2000으로 저장
        elif len(filters) == 1 and filters[0][0] in LITERALS_JPX_DECODE:
            name = self._save_jpeg2000(image)

        # 이미지가 JBIG2 형식인 경우 JBIG2로 저장
        elif self._is_jbig2_iamge(image):
            name = self._save_jbig2(image)

        # 이미지가 1비트 단위인 경우 BMP로 저장
        elif image.bits == 1:
            name = self._save_bmp(image, width, height, (width + 7) // 8, image.bits)

        # 이미지가 8비트 단위이고 RGB 컬러스페이스를 사용하는 경우 BMP로 저장
        elif image.bits == 8 and LITERAL_DEVICE_RGB in image.colorspace:
            name = self._save_bmp(image, width, height, width * 3, image.bits * 3)

        # 이미지가 8비트 단위이고 그레이스케일 컬러스페이스를 사용하는 경우 BMP로 저장
        elif image.bits == 8 and LITERAL_DEVICE_GRAY in image.colorspace:
            name = self._save_bmp(image, width, height, width, image.bits)

        # 필터가 하나이고, 그 필터가 Flate 디코딩을 사용하는 경우 바이트로 저장
        elif len(filters) == 1 and filters[0][0] in LITERALS_FLATE_DECODE:
            name = self._save_bytes(image)

        # 그 외의 경우 raw 데이터로 저장
        else:
            name = self._save_raw(image)

        # 저장된 이미지 파일의 이름을 반환
        return name


    def _save_jpeg(self, image: LTImage) -> str:
    # JPEG 인코딩된 이미지를 저장
    #"""Save a JPEG encoded image"""
    
    # 이미지에서 raw 데이터를 추출
        raw_data = image.stream.get_rawdata()
        
        # raw 데이터가 None이 아님을 확인
        assert raw_data is not None

        # 이미지 파일의 고유한 이름을 생성
        name, path = self._create_unique_image_name(image, ".jpg")
        
        # 파일을 쓰기 모드로 열고
        with open(path, "wb") as fp:
            # 이미지의 컬러스페이스가 CMYK인 경우
            if LITERAL_DEVICE_CMYK in image.colorspace:
                # PIL 라이브러리를 import 시도
                try:
                    from PIL import Image, ImageChops  # type: ignore[import]
                except ImportError:
                    # PIL 라이브러리가 없으면 오류 메시지를 출력
                    raise ImportError(PIL_ERROR_MESSAGE)

                # raw 데이터를 BytesIO 객체로 변환
                ifp = BytesIO(raw_data)
                
                # 이미지를 열고
                i = Image.open(ifp)
                
                # 이미지를 반전시키고
                i = ImageChops.invert(i)
                
                # 이미지를 RGB로 변환한 후
                i = i.convert("RGB")
                
                # 이미지를 JPEG 형식으로 저장
                i.save(fp, "JPEG")
            else:
                # 이미지의 컬러스페이스가 CMYK가 아닌 경우, raw 데이터를 그대로 파일에 쓰기
                fp.write(raw_data)

        # 저장된 이미지 파일의 이름을 반환
        return name


    def _save_jpeg2000(self, image: LTImage) -> str:
        """Save a JPEG 2000 encoded image"""
        raw_data = image.stream.get_rawdata()
        assert raw_data is not None

        name, path = self._create_unique_image_name(image, ".jp2")
        with open(path, "wb") as fp:
            try:
                from PIL import Image  # type: ignore[import]
            except ImportError:
                raise ImportError(PIL_ERROR_MESSAGE)

            # if we just write the raw data, most image programs
            # that I have tried cannot open the file. However,
            # open and saving with PIL produces a file that
            # seems to be easily opened by other programs
            ifp = BytesIO(raw_data)
            i = Image.open(ifp)
            i.save(fp, "JPEG2000")
        return name

    def _save_jbig2(self, image: LTImage) -> str:
        """Save a JBIG2 encoded image"""
        name, path = self._create_unique_image_name(image, ".jb2")
        with open(path, "wb") as fp:
            input_stream = BytesIO()

            global_streams = []
            filters = image.stream.get_filters()
            for filter_name, params in filters:
                if filter_name in LITERALS_JBIG2_DECODE:
                    global_streams.append(params["JBIG2Globals"].resolve())

            if len(global_streams) > 1:
                msg = (
                    "There should never be more than one JBIG2Globals "
                    "associated with a JBIG2 embedded image"
                )
                raise ValueError(msg)
            if len(global_streams) == 1:
                input_stream.write(global_streams[0].get_data().rstrip(b"\n"))
            input_stream.write(image.stream.get_data())
            input_stream.seek(0)
            reader = JBIG2StreamReader(input_stream)
            segments = reader.get_segments()

            writer = JBIG2StreamWriter(fp)
            writer.write_file(segments)
        return name

    def _save_bmp(
        self, image: LTImage, width: int, height: int, bytes_per_line: int, bits: int
    ) -> str:
        """Save a BMP encoded image"""
        name, path = self._create_unique_image_name(image, ".bmp")
        with open(path, "wb") as fp:
            bmp = BMPWriter(fp, bits, width, height)
            data = image.stream.get_data()
            i = 0
            for y in range(height):
                bmp.write_line(y, data[i : i + bytes_per_line])
                i += bytes_per_line
        return name

    def _save_bytes(self, image: LTImage) -> str:
        """Save an image without encoding, just bytes"""
        name, path = self._create_unique_image_name(image, ".jpg")
        width, height = image.srcsize
        channels = len(image.stream.get_data()) / width / height / (image.bits / 8)
        with open(path, "wb") as fp:
            try:
                from PIL import Image  # type: ignore[import]
                from PIL import ImageOps
            except ImportError:
                raise ImportError(PIL_ERROR_MESSAGE)

            mode: Literal["1", "L", "RGB", "CMYK"]
            if image.bits == 1:
                mode = "1"
            elif image.bits == 8 and channels == 1:
                mode = "L"
            elif image.bits == 8 and channels == 3:
                mode = "RGB"
            elif image.bits == 8 and channels == 4:
                mode = "CMYK"

            img = Image.frombytes(mode, image.srcsize, image.stream.get_data(), "raw")
            if mode == "L":
                img = ImageOps.invert(img)

            img.save(fp)

        return name

    def _save_raw(self, image: LTImage) -> str:
        """Save an image with unknown encoding"""
        ext = ".%d.%dx%d.img" % (image.bits, image.srcsize[0], image.srcsize[1])
        name, path = self._create_unique_image_name(image, ext)

        with open(path, "wb") as fp:
            fp.write(image.stream.get_data())
        return name

    @staticmethod
    def _is_jbig2_iamge(image: LTImage) -> bool:
        filters = image.stream.get_filters()
        for filter_name, params in filters:
            if filter_name in LITERALS_JBIG2_DECODE:
                return True
        return False

    def _create_unique_image_name(self, image: LTImage, ext: str) -> Tuple[str, str]:
        name = image.name + ext
        path = os.path.join(self.outdir, name)
        img_index = 0
        while os.path.exists(path):
            name = "%s.%d%s" % (image.name, img_index, ext)
            path = os.path.join(self.outdir, name)
            img_index += 1
        return name, path
