import binascii
import ctypes
import struct
import sys


def tohex(val, nbits):
    """Utility to convert (signed) integer to hex."""
    return hex((val + (1 << nbits)) % (1 << nbits))


def decompress(data):
    NULL = ctypes.POINTER(ctypes.c_uint)()
    SIZE_T = ctypes.c_uint
    DWORD = ctypes.c_uint32
    USHORT = ctypes.c_uint16
    UCHAR = ctypes.c_ubyte
    ULONG = ctypes.c_uint32

    # You must have at least Windows 8, or it should fail.
    try:
        RtlDecompressBufferEx = ctypes.windll.ntdll.RtlDecompressBufferEx
    except AttributeError:
        sys.exit('You must have Windows with version >=8.')

    RtlGetCompressionWorkSpaceSize = \
        ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize

    with open(data, 'rb') as fin:
        header = fin.read(8)
        compressed = fin.read()

        signature, decompressed_size = struct.unpack('<LL', header)
        calgo = (signature & 0x0F000000) >> 24
        crcck = (signature & 0xF0000000) >> 28
        magic = signature & 0x00FFFFFF
        if magic != 0x004d414d:
            sys.exit('Wrong signature... wrong file?')

        if crcck:
            # I could have used RtlComputeCrc32.
            file_crc = struct.unpack('<L', compressed[:4])[0]
            crc = binascii.crc32(header)
            crc = binascii.crc32(struct.pack('<L', 0), crc)
            compressed = compressed[4:]
            crc = binascii.crc32(compressed, crc)
            if crc != file_crc:
                sys.exit('Wrong file CRC {0:x} - {1:x}!'.format(crc, file_crc))

        compressed_size = len(compressed)

        ntCompressBufferWorkSpaceSize = ULONG()
        ntCompressFragmentWorkSpaceSize = ULONG()

        ntstatus = RtlGetCompressionWorkSpaceSize(USHORT(calgo),
                                                  ctypes.byref(ntCompressBufferWorkSpaceSize),
                                                  ctypes.byref(ntCompressFragmentWorkSpaceSize))

        if ntstatus:
            sys.exit('Cannot get workspace size, err: {}'.format(
                tohex(ntstatus, 32)))

        ntCompressed = (UCHAR * compressed_size).from_buffer_copy(compressed)
        ntDecompressed = (UCHAR * decompressed_size)()
        ntFinalUncompressedSize = ULONG()
        ntWorkspace = (UCHAR * ntCompressFragmentWorkSpaceSize.value)()

        ntstatus = RtlDecompressBufferEx(
            USHORT(calgo),
            ctypes.byref(ntDecompressed),
            ULONG(decompressed_size),
            ctypes.byref(ntCompressed),
            ULONG(compressed_size),
            ctypes.byref(ntFinalUncompressedSize),
            ctypes.byref(ntWorkspace))

        if ntstatus:
            sys.exit('Decompression failed, err: {}'.format(
                tohex(ntstatus, 32)))

        if ntFinalUncompressedSize.value != decompressed_size:
            print('Decompressed with a different size than original!')

        return bytearray(ntDecompressed)