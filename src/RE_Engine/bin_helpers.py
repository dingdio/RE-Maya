import struct
import math

class TypeFormat:
    SByte = '<b'
    Byte = '<B'
    Int16 = '<h'
    UInt16 = '<H'
    Int32 = '<i'
    UInt32 = '<I'
    Int64 = '<l'
    UInt64 = '<L'
    Single = '<f'
    Double = '<d'

def findEndOfMot(f):
    while (f.tell()+4 < FileSize(f)):
        filesize = FileSize(f)
        tell = f.tell();
        if (f.tell() == 544501613):
            f.seek(-4, 1); break;
        f.seek(1, 1);

def FileSize(f):
    old_file_position = f.tell()
    f.seek(0, 2)
    size = f.tell()
    f.seek(old_file_position, 0)
    return size

def readString(inFile):
    chars = []
    while True:
        c = inFile.read(1)
        if c == chr(0):
            return "".join(chars)
        chars.append(c)

# def getString(file):
#     result = ""
#     tmpChar = file.read(1)
#     while ord(tmpChar) != 0:
#         result += tmpChar.decode('utf-8')
#         tmpChar =file.read(1)
#     return result

def read_wstring(inFile, chunk_len = 0x100, address = 0):
    #.replace("\x00","")
    if address == 0:
        address = inFile.tell()
    wstring = ''
    offset = 0
    stringSize = 0
    while 1:
        null_found = False
        inFile.seek(address+offset)
        read_bytes = inFile.read(chunk_len)
        for i in range(0, len(read_bytes)-1, 2):
            if read_bytes[i] == '\x00' and read_bytes[i+1] == '\x00':
                null_found = True
                stringSize += i+2
                break
            wstring += read_bytes[i]

        if null_found:
            break
        offset += len(read_bytes)
        if offset > 9999: # wut
            break
    inFile.seek(address+stringSize+offset)
    return wstring

def readU32(inFile):
    return struct.unpack('I', inFile.read(4))[0]

def readInt16(file):
    return struct.unpack(TypeFormat.Int16, file.read(2))[0]

def readUShort(file):
    return struct.unpack(TypeFormat.UInt16, file.read(2))[0]

def readUByte(file):
    return struct.unpack(TypeFormat.Byte, file.read(1))[0]

def readI32(inFile):
    return struct.unpack('i', inFile.read(4))[0]

def readULong(inFile):
    return struct.unpack('L', inFile.read(4))[0]

def readU64(inFile):
    return struct.unpack('Q', inFile.read(8))[0]

def readFloat(inFile):
    return struct.unpack('f', inFile.read(4))[0]

# def readSingle(file):
#     numberBin = file.read(4)
#     single = struct.unpack(TypeFormat.Single, numberBin)[0]
#     return single

def skipToNextLine(f):
    while (f.tell() %16 != 0):
        f.seek(1, 1)

def wRot(frame):
    RotationX = frame.RotationX
    RotationY = frame.RotationY
    RotationZ = frame.RotationZ

    RotationW = 1.0 - (RotationX * RotationX + RotationY * RotationY + RotationZ * RotationZ)
    if (RotationW > 0.0):
        RotationW = math.sqrt(RotationW) #(float)Sqrt(RotationW);
    else:
        RotationW = 0.0;
    return RotationW;