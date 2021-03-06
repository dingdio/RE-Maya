import struct
import math
import re_import_mot
reload(re_import_mot)

from bin_helpers import (
                        #findEndOfMot,
                        FileSize,
                        #readString,
                        #getString,
                        read_wstring,
                        readU32,
                        readInt16,
                        readUShort,
                        readUByte,
                        readI32,
                        readULong,
                        readU64,
                        readFloat,
                        #readSingle,
                        skipToNextLine,
                        wRot)

bIsMotFile = False
boneHeadersIdx = 0 #1st mot file with bone list
#/* ----DEFINITIONS---- */
#define TRANSLATION (1)
#define ROTATION (1 << 1)
#define SCALE (1 << 2)

def get_translation_type(f, MOT):
    flagsEval = f & 0xFF000
    if MOT.MOT_HEADER.version == 65 or MOT.MOT_HEADER.version == 43:
        if flagsEval == 0x00000: return "LoadVector3sFull"
        if flagsEval == 0x20000: return "LoadVector3s5BitA"
        if flagsEval == 0x30000: return "LoadVector3s10BitA"
        if flagsEval == 0x40000: return "LoadVector3s10BitA"
        if flagsEval == 0x70000: return "LoadVector3s21BitA"
        if flagsEval == 0x31000: return "LoadVector3sXAxis"
        if flagsEval == 0x32000: return "LoadVector3sYAxis"
        if flagsEval == 0x33000: return "LoadVector3sZAxis"
        if flagsEval == 0x21000: return "LoadVector3sXAxis16Bit"
        if flagsEval == 0x22000: return "LoadVector3sYAxis16Bit"
        if flagsEval == 0x23000: return "LoadVector3sZAxis16Bit"
        return "Unknown Type"
    else:
        if flagsEval == 0x00000: return "LoadVector3sFull"
        if flagsEval == 0x20000: return "LoadVector3s5BitB"
        if flagsEval == 0x30000: return "LoadVector3s5BitB"
        if flagsEval == 0x40000: return "LoadVector3s10BitB"
        if flagsEval == 0x80000: return "LoadVector3s21BitB"
        if flagsEval == 0x21000: return "LoadVector3sXAxis16Bit"
        if flagsEval == 0x22000: return "LoadVector3sYAxis16Bit"
        if flagsEval == 0x23000: return "LoadVector3sZAxis16Bit"
        if flagsEval == 0x24000: return "LoadVector3sXYZAxis16Bit"
        if flagsEval == 0x41000: return "LoadVector3sXAxis"
        if flagsEval == 0x42000: return "LoadVector3sYAxis"
        if flagsEval == 0x43000: return "LoadVector3sZAxis"
        if flagsEval == 0x44000: return "LoadVector3sXYZAxis"
        return "Unknown Type"

def get_rotation_type(f, MOT):
    flagsEval = f & 0xFF000
    if MOT.MOT_HEADER.version == 65 or MOT.MOT_HEADER.version == 43:
        #//RE2 and RE7
        if flagsEval == 0x00000: return "LoadQuaternionsFull"
        if flagsEval == 0xB0000: return "LoadQuaternions3Component"
        if flagsEval == 0xC0000: return "LoadQuaternions3Component"
        if flagsEval == 0x30000: return "LoadQuaternions10Bit"
        if flagsEval == 0x40000: return "LoadQuaternions10Bit"
        if flagsEval == 0x50000: return "LoadQuaternions16Bit"
        if flagsEval == 0x70000: return "LoadQuaternions21Bit"
        if flagsEval == 0x21000: return "LoadQuaternionsXAxis16Bit"
        if flagsEval == 0x22000: return "LoadQuaternionsYAxis16Bit"
        if flagsEval == 0x23000: return "LoadQuaternionsZAxis16Bit"
        if flagsEval == 0x31000: return "LoadQuaternionsXAxis"
        if flagsEval == 0x41000: return "LoadQuaternionsXAxis"
        if flagsEval == 0x32000: return "LoadQuaternionsYAxis"
        if flagsEval == 0x42000: return "LoadQuaternionsYAxis"
        if flagsEval == 0x33000: return "LoadQuaternionsZAxis"
        if flagsEval == 0x43000: return "LoadQuaternionsZAxis"
        return "Unknown Type"
    else:
        if flagsEval == 0x00000: return "LoadQuaternionsFull"
        if flagsEval == 0xB0000: return "LoadQuaternions3Component"
        if flagsEval == 0xC0000: return "LoadQuaternions3Component"
        if flagsEval == 0x20000: return "LoadQuaternions5Bit"
        if flagsEval == 0x30000: return "LoadQuaternions8Bit"
        if flagsEval == 0x40000: return "LoadQuaternions10Bit"
        if flagsEval == 0x50000: return "LoadQuaternions13Bit"
        if flagsEval == 0x60000: return "LoadQuaternions16Bit"
        if flagsEval == 0x70000: return "LoadQuaternions18Bit"
        if flagsEval == 0x80000: return "LoadQuaternions21Bit"
        if flagsEval == 0x40000: return "LoadQuaternions10Bit"
        if flagsEval == 0x21000: return "LoadQuaternionsXAxis16Bit"
        if flagsEval == 0x22000: return "LoadQuaternionsYAxis16Bit"
        if flagsEval == 0x23000: return "LoadQuaternionsZAxis16Bit"
        if flagsEval == 0x31000: return "LoadQuaternionsXAxis"
        if flagsEval == 0x41000: return "LoadQuaternionsXAxis"
        if flagsEval == 0x32000: return "LoadQuaternionsYAxis"
        if flagsEval == 0x42000: return "LoadQuaternionsYAxis"
        if flagsEval == 0x33000: return "LoadQuaternionsZAxis"
        if flagsEval == 0x43000: return "LoadQuaternionsZAxis"
        return "Unknown Type"

def get_scale_type(f, MOT):
    flagsEval = f & 0xFF000
    if flagsEval == 0x00000: return "LoadVector3sFull"
    if flagsEval == 0x20000: return "LoadVector3s5BitA"
    if flagsEval == 0x30000: return "LoadVector3s10BitA"
    if flagsEval == 0x34000: return "LoadScalesXYZ"
    if flagsEval == 0x40000: return "LoadVector3s10BitA"
    if flagsEval == 0x70000: return "LoadVector3s21BitA"
    if flagsEval == 0x31000: return "LoadVector3sXAxis"
    if flagsEval == 0x32000: return "LoadVector3sYAxis"
    if flagsEval == 0x33000: return "LoadVector3sZAxis"
    if flagsEval == 0x21000: return "LoadVector3sXAxis16Bit"
    if flagsEval == 0x22000: return "LoadVector3sYAxis16Bit"
    if flagsEval == 0x23000: return "LoadVector3sZAxis16Bit"
    return "Unknown Type"

class Pointer:
    def __init__(self,f):
        self.Address = readU64(f)

        ##get string and return
        pos = f.tell()
        self.motName = read_wstring(f, address= self.Address + 116)
        f.seek(pos)

        if self.Address == 0:
            self.motName = ""

class BoneHeader:
    def __init__(self,f, start):
        self.boneNameOffs = readU64(f)
        position = f.tell()
        f.seek(self.boneNameOffs + start)
        self.boneName = read_wstring(f)
        f.seek(position)
        self.parentOffs = readU64(f)
        self.childOffs = readU64(f)
        self.nextSiblingOffs = readU64(f)

        self.translation = [ readFloat(f), readFloat(f), readFloat(f), readFloat(f) ]
        self.quaternion = [ readFloat(f), readFloat(f), readFloat(f), readFloat(f) ]

        self.Index = readU32(f)
        self.boneHash = readU32(f)   # uint   //MurMur3
        self.padding = readU64(f)
        # uint64 padding;

class BoneName:
    def __init__(self, f, start):
        self.String = read_wstring(f)

class BoneHeaders:
    def __init__(self, f, start):
        self.boneHdrOffs = readU64(f)
        self.boneHdrCount = readU64(f)
        if (self.boneHdrCount <= 1000):
            self.BONE_HEADER = []
            for i in range(0, self.boneHdrCount):
                self.BONE_HEADER.append(BoneHeader(f, start))

            self.BONE_NAME = []
            for i in range(0, self.boneHdrCount):
                self.BONE_NAME.append(BoneName(f, start))

class BoneClipHeader:
    def __init__(self, f, MOT):
        start = MOT.start
        MOT_HEADER = MOT.MOT_HEADER
        BONE_HEADERS = MOT.BONE_HEADERS
        MOT_LIST = MOT.MOT_LIST
        if (MOT_HEADER.version == 65):
            self.boneIndex = readUShort(f); #ushort
            self.trackFlags = readUShort(f); #trckFlg_t  #// flags for type: translations ?+    rotations xor scales
            self.boneHash = readU32(f); #uint32       # // MurMur3
            self.uknFloat = readFloat(f); #float      # // always 1.0?
            self.padding = readI32(f); #uint32
            self.trackHdrOffs = readU64(f); #uint64  # //keysPointer
        elif (MOT_HEADER.version == 78 or MOT_HEADER.version == 43):
            self.boneIndex = readUShort(f); #ushort
            self.trackFlags = readUShort(f); #trckFlg_t  #// flags for type: translations ?+    rotations xor scales
            self.boneHash = readU32(f); #uint32       # // MurMur3
            if MOT_HEADER.version == 43:
                self.trackHdrOffs = readU64(f)
            else:
                self.trackHdrOffs = readU32(f)

        if hasattr(BONE_HEADERS, 'BONE_HEADER'):
            for x in BONE_HEADERS.BONE_HEADER:
                if x.boneHash == self.boneHash:
                    self.name = x.boneName
                    break
        else:
            for x in MOT_LIST[boneHeadersIdx].BONE_HEADERS.BONE_HEADER:
                if x.boneHash == self.boneHash:
                    self.name = x.boneName
                    break

class Keys:
    def __init__(self, f, keyCount, flags, frameDataOffs): #uint32 keyCount, uint32 flags, uint64 frameDataOffs
        self.frameIndex = []
        if flags >> 20 == 2:
            for i in range(0, keyCount):
                self.frameIndex.append(readUByte(f))
            #ubyte frameIndex[keyCount]
        elif flags >> 20 == 4:
            for i in range(0, keyCount):
                self.frameIndex.append(readInt16(f))
            #int16 frameIndex[keyCount]
        elif flags >> 20 == 5:
            for i in range(0, keyCount):
                self.frameIndex.append(readI32(f))
            #int32 frameIndex[keyCount]

class VectorFull(object):
    def __init__(self, vector):
        self.vector = vector
        self.vectorRead = self.vector #* 100.0 # dunno why this was here
    def VectorRead(self):
        return self.vectorRead

    def VectorWrite(self):
        pass
    # void VectorWrite( VectorFull &f, string s ) {
    #     local float ff = Atof(s);
    #     f = (VectorFull )( (float)(ff / 100.0) );
    # }

class Frame:
    def __init__(self, f, MOT, keyCount, flags, frame, FrameDataTrns): #uint32 keyCount, uint32 flags
        start = MOT.start
        MOT_HEADER = MOT.MOT_HEADER
        if hasattr(FrameDataTrns, 'unpackData'):
            unpackData = FrameDataTrns.unpackData
        else:
            pass
            #print("find unpack? should be LoadVector3sFull")
        ##unpackData = FrameDataTrns.unpackData
        if hasattr(FrameDataTrns, 'KEYS'):
            Time = FrameDataTrns.KEYS.frameIndex[frame];
            flagsEval = flags & 0xFF000
            if (flagsEval == 0x00000): #//LoadVector3sFull
              self.X = VectorFull(readFloat(f)).VectorRead()
              self.Y = VectorFull(readFloat(f)).VectorRead()
              self.Z = VectorFull(readFloat(f)).VectorRead()
              return; #'VectorFull TranslationX, TranslationZ, TranslationY;

            if (flagsEval == 0x20000):
                self.TranslationData = readUShort(f) #if (SKIP) break; # ushort
                if (MOT_HEADER.version == 65 or MOT_HEADER.version == 43): #//LoadVector3s5BitA RE2
                    self.X = unpackData[0] * (((self.TranslationData >> 00) & 0x1F) * (1.0 / 0x1F)) + unpackData[4] #local float
                    self.Y = unpackData[1] * (((self.TranslationData >> 05) & 0x1F) * (1.0 / 0x1F)) + unpackData[5] #local float
                    self.Z = unpackData[2] * (((self.TranslationData >> 10) & 0x1F) * (1.0 / 0x1F)) + unpackData[6] #local float
                else: #                        //LoadVector3s5BitB RE3
                    self.X = unpackData[0] * (((self.TranslationData >> 00) & 0x1F) * (1.0 / 0x1F)) + unpackData[3] #local float
                    self.Y = unpackData[1] * (((self.TranslationData >> 05) & 0x1F) * (1.0 / 0x1F)) + unpackData[4] #local float
                    self.Z = unpackData[2] * (((self.TranslationData >> 10) & 0x1F) * (1.0 / 0x1F)) + unpackData[5] #local float
                return;

            if (flagsEval == 0x34000):
                if (MOT_HEADER.version == 65): #//LoadScalesXYZ RE2
                    self.X = readFloat(f)#float X;
                    self.Y = self.X #local float Y = X;
                    self.Z = self.X #local float Z = X;
                    return#break;


            if (flagsEval == 0x30000):                       #//LoadVector3s10BitA RE2
                if (MOT_HEADER.version == 78): #//LoadVector3s5BitB RE3
                    self.TranslationData = readUShort(f); # #if (SKIP) break;
                    self.X = unpackData[0] * (((self.TranslationData >> 00) & 0x1F) * (1.0 / 0x1F)) + unpackData[3]
                    self.Y = unpackData[1] * (((self.TranslationData >> 05) & 0x1F) * (1.0 / 0x1F)) + unpackData[4]
                    self.Z = unpackData[2] * (((self.TranslationData >> 10) & 0x1F) * (1.0 / 0x1F)) + unpackData[5]
                    return

            if (flagsEval == 0x40000):
                self.TranslationData = readU32(f) #uint32  #if (SKIP) break;
                if (MOT_HEADER.version == 65 or MOT_HEADER.version == 43): #//LoadVector3s10BitA RE2
                    self.X = unpackData[0] * (((self.TranslationData >> 00) & 0x3FF) * (1.0 / 0x3FF)) + unpackData[4];
                    self.Y = unpackData[1] * (((self.TranslationData >> 10) & 0x3FF) * (1.0 / 0x3FF)) + unpackData[5];
                    self.Z = unpackData[2] * (((self.TranslationData >> 20) & 0x3FF) * (1.0 / 0x3FF)) + unpackData[6];
                else: #                        //LoadVector3s10BitB RE3
                    self.X = unpackData[0] * (((self.TranslationData >> 00) & 0x3FF) * (1.0 / 0x3FF)) + unpackData[3];
                    self.Y = unpackData[1] * (((self.TranslationData >> 10) & 0x3FF) * (1.0 / 0x3FF)) + unpackData[4];
                    self.Z = unpackData[2] * (((self.TranslationData >> 20) & 0x3FF) * (1.0 / 0x3FF)) + unpackData[5];
                return;

            if (flagsEval == 0x70000):                     #  //LoadVector3s21BitA  RE2
                self.TranslationData = readU64(f) #uint64 #if (SKIP) break;
                self.X = unpackData[0] * (((self.TranslationData >> 00) & 0x1FFFFF) / 2097151.0) + unpackData[4];
                self.Y = unpackData[1] * (((self.TranslationData >> 21) & 0x1FFFFF) / 2097151.0) + unpackData[5];
                self.Z = unpackData[2] * (((self.TranslationData >> 42) & 0x1FFFFF) / 2097151.0) + unpackData[6];
                return;

            if (flagsEval == 0x80000):                 #      //LoadVector3s21BitB  RE3
                self.TranslationData = readU64(f) #uint64 #if (SKIP) break;
                self.X = unpackData[0] * (((self.TranslationData >> 00) & 0x1FFFFF) / 2097151.0) + unpackData[3];
                self.Y = unpackData[1] * (((self.TranslationData >> 21) & 0x1FFFFF) / 2097151.0) + unpackData[4];
                self.Z = unpackData[2] * (((self.TranslationData >> 42) & 0x1FFFFF) / 2097151.0) + unpackData[5];
                return;

            if (flagsEval == 0x31000 or flagsEval == 0x41000):  #                     //LoadVector3sXAxis RE2   // RE3
                self.X = readFloat(f);
                self.Y = unpackData[1];
                self.Z = unpackData[2];
                return;

            if (flagsEval == 0x32000 or flagsEval == 0x42000):  #                     //LoadVector3sYAxis RE2   // RE3
                self.X = unpackData[0];
                self.Y = readFloat(f) # float
                self.Z = unpackData[2];
                return;

            if (flagsEval == 0x33000 or flagsEval == 0x43000):   #                    //LoadVector3sZAxis RE2 // RE3
                self.X = unpackData[0];
                self.Y = unpackData[1];
                self.Z = readFloat(f) #float
                return;

            if (flagsEval == 0x21000):                   #    //LoadVector3sXAxis16Bit
                self.TranslationData =readUShort(f)# ushort  #if (SKIP) break;
                self.X = unpackData[0] * (self.TranslationData / 65535.0) + unpackData[1];
                self.Y = unpackData[2];
                self.Z = unpackData[3];
                return;

            if (flagsEval == 0x22000):         #              //LoadVector3sYAxis16Bit
                self.TranslationData = readUShort(f)# #if (SKIP) break;
                self.X = unpackData[1];
                self.Y = unpackData[0] * (self.TranslationData / 65535.0) + unpackData[2];
                self.Z = unpackData[3];
                return;

            if (flagsEval == 0x23000):     #                  //LoadVector3sZAxis16Bit
                self.TranslationData  = readUShort(f)# #if (SKIP) break;
                self.X = unpackData[1];
                self.Y = unpackData[2];
                self.Z = unpackData[0] * (self.TranslationData / 65535.0) + unpackData[3];
                return;

            if (flagsEval == 0x24000):                      # //LoadVector3sXYZAxis16Bit RE3
                self.TranslationData = readUShort(f)# #if (SKIP) break;
                self.X = unpackData[0] * (self.TranslationData / 65535.0) + unpackData[3];
                self.Y = self.X
                self.Z = self.X
                return;

            if (flagsEval == 0x44000):                      # //LoadVector3sXYZAxis RE3
                self.TranslationData = readFloat(f)
                self.X = self.TranslationData;
                self.Y = self.TranslationData;
                self.Z = self.TranslationData;
                return;

            print ("uh oh")
            # # default:
            #Printf("Unknown Translation Type: %x at FTell %d\n", (flags & 0xFF000), FTell());

class FrameDataTrns:
    def __init__(self, f, MOT, keyCount,flags,frameDataOffs,unpackDataOffs,frameIndOffs):
        start = MOT.start
    #uint32 keyCount, uint32 flags, uint64 frameDataOffs, uint64 unpackDataOffs, uint64 frameIndOffs
        if (frameIndOffs > 0):
            f.seek(frameIndOffs);
            self.KEYS = Keys(f, keyCount, flags, frameDataOffs)
        if (unpackDataOffs > start):
            f.seek(unpackDataOffs);
            self.unpackData = [readFloat(f),readFloat(f),readFloat(f),readFloat(f),readFloat(f),readFloat(f),readFloat(f),readFloat(f)]; #float
            pos2 = f.tell();
        else:
            pass
            #print("No unpack data")
        f.seek(frameDataOffs);

        ###STUFF HERE
        self.Frames = []
        for frame in range(0, keyCount):
            self.Frames.append(Frame(f, MOT, keyCount, flags, frame, self))

        if (unpackDataOffs > start):
            f.seek(pos2);

class FrameRot:
    def __init__(self, f, MOT, keyCount, flags, frame, framedatarot, CUR_BONE_NAME): #uint32 keyCount, uint32 flags
        start = MOT.start
        self.RotationTypeString = get_rotation_type(flags, MOT)
        self.CUR_BONE_NAME = CUR_BONE_NAME
        if hasattr(framedatarot, 'unpackData'):
            MinUnpackX = framedatarot.unpackData[4]
            MinUnpackY = framedatarot.unpackData[5]
            MinUnpackZ = framedatarot.unpackData[6]
            MinUnpackW = framedatarot.unpackData[7]

            MaxUnpackX = framedatarot.unpackData[0]
            MaxUnpackY = framedatarot.unpackData[1]
            MaxUnpackZ = framedatarot.unpackData[2]
            MaxUnpackW = framedatarot.unpackData[3]

        else:
            pass
            #print("find unpack? should be LoadVector3sFull")

        MOT_HEADER = MOT.MOT_HEADER
        ##unpackData = framedatarot.unpackData
        if hasattr(framedatarot, 'KEYS'):
            self.inverse = False
            self.Time = framedatarot.KEYS.frameIndex[frame];
            flagsEval = flags & 0xFF000

            if (flagsEval == 0x00000): #//LoadQuaternionsFull
                self.RotationX = readFloat(f)
                self.RotationY = readFloat(f)
                self.RotationZ = readFloat(f)
                self.RotationW = readFloat(f)
                return;

            # case 0x00000:
            #     float RotationX, RotationY, RotationZ, RotationW;
            #     break;

            if (flagsEval == 0xB0000 or flagsEval == 0xC0000):             #          //LoadQuaternions3Component
                self.RotationX = readFloat(f);
                self.RotationY = readFloat(f);
                self.RotationZ = readFloat(f); #if (SKIP) break;
                self.RotationW = wRot(self); # local float
                return;

            if (flagsEval == 0x20000):             #          //LoadQuaternions5Bit RE3
                RotationData = readUShort(f)#ushort  #if (SKIP) return;
                self.RotationX = (MaxUnpackX * ((RotationData >> 00) & 0x1F) * (1.0 / 0x1F)) + MinUnpackX;
                self.RotationY = (MaxUnpackY * ((RotationData >> 05) & 0x1F) * (1.0 / 0x1F)) + MinUnpackY;
                self.RotationZ = (MaxUnpackZ * ((RotationData >> 10) & 0x1F) * (1.0 / 0x1F)) + MinUnpackZ;
                self.RotationW = wRot(self);
                return;

            #BiLinearSCQuat3_16bitController in revilmax
            if (flagsEval == 0x21000):             #          //LoadQuaternionsXAxis16Bit ##static constexpr uint32 ID1 = 0x21112; Revilmax
                #RotationData = readUShort(f)#ushort #if (SKIP) return;
                RotationData = readUShort(f)#ushort #if (SKIP) return;
                self.RotationX = MaxUnpackX * (RotationData / 65535.0) + MaxUnpackY; ##CHANGED LOOK INTO
                self.RotationY = 0.0;
                self.RotationZ = 0.0;
                self.RotationW = wRot(self);

                # check = 1.0 - (self.RotationX * self.RotationX + self.RotationY * self.RotationY + self.RotationZ * self.RotationZ)
                # if check < 0:
                #     self.inverse = True
                #     self.RotationW = 2.0
                return;

            if (flagsEval == 0x22000):             #          //LoadQuaternionsYAxis16Bit
                RotationData = readUShort(f)#ushort #if (SKIP) return;
                self.RotationX = 0.0;
                self.RotationY = MaxUnpackX * (RotationData / 65535.0) + MaxUnpackY; ##CHANGED LOOK INTO
                self.RotationZ = 0.0;
                self.RotationW = wRot(self);
                return;

            if (flagsEval == 0x23000):             #          //LoadQuaternionsZAxis16Bit
                RotationData = readUShort(f)#ushort #if (SKIP) return;
                self.RotationX = 0.0;
                self.RotationY = 0.0;
                self.RotationZ = MaxUnpackX * (RotationData / 65535.0) + MaxUnpackY; ##CHANGED LOOK INTO
                self.RotationW = wRot(self);
                return;

            if (flagsEval == 0x30000):             #          //LoadQuaternions10Bit RE2
                if (MOT_HEADER.version == 78):#/LoadQuaternions8Bit RE3
                    RotationDataX = readUByte(f)#ubyte RotationDataX, RotationDataY, RotationDataZ; #if (SKIP) return;
                    RotationDataY = readUByte(f)
                    RotationDataZ = readUByte(f)
                    componentMultiplier = 1.0 / 0xff;
                    self.RotationX = ((RotationDataX * componentMultiplier) * MaxUnpackX) + MinUnpackX#(MaxUnpackX * (RotationDataX * 0.000015259022)) + MinUnpackX;
                    self.RotationY = ((RotationDataY * componentMultiplier) * MaxUnpackY) + MinUnpackY#(MaxUnpackY * (RotationDataY * 0.000015259022)) + MinUnpackY;
                    self.RotationZ = ((RotationDataZ * componentMultiplier) * MaxUnpackZ) + MinUnpackZ#(MaxUnpackZ * (RotationDataZ * 0.000015259022)) + MinUnpackZ;
                    self.RotationX = self.RotationX*1.0
                    self.RotationY = self.RotationY*1.0
                    self.RotationZ = self.RotationZ*1.0
                    self.RotationW = wRot(self);
                    return;
            if (flagsEval == 0x40000 or (MOT_HEADER.version == 65 and flagsEval == 0x30000)):             #          //LoadQuaternions10Bit RE3 #TEETH ROT
                RotationData = readU32(f) #uint32  #if (SKIP) return;
                componentMultiplier = 1.0 / 0x3FF;
                self.RotationX = (MaxUnpackX * ((RotationData >> 00) & 0x3FF) / 1023.0) + MinUnpackX;
                self.RotationY = (MaxUnpackY * ((RotationData >> 10) & 0x3FF) / 1023.0) + MinUnpackY;
                self.RotationZ = (MaxUnpackZ * ((RotationData >> 20) & 0x3FF) / 1023.0) + MinUnpackZ;
                self.RotationW = wRot(self);
                return;

            if (flagsEval == 0x31000 or flagsEval == 0x41000):             #          //LoadQuaternionsXAxis
                self.RotationX = readFloat(f) #float
                self.RotationY = 0.0;
                self.RotationZ = 0.0; #if (SKIP) return;
                self.RotationW = wRot(self);
                return;

            if (flagsEval == 0x32000 or flagsEval == 0x42000):             #          //LoadQuaternionsYAxis
                self.RotationX = 0.0;
                self.RotationY = readFloat(f)
                self.RotationZ = 0.0; #if (SKIP) return;
                self.RotationW = wRot(self);
                return;

            if (flagsEval == 0x33000 or flagsEval == 0x43000):             #          //LoadQuaternionsZAxis
                self.RotationX = 0.0;
                self.RotationY = 0.0;
                self.RotationZ = readFloat(f); #if (SKIP) return;
                self.RotationW = wRot(self);
                return;

            if (flagsEval == 0x50000):             #          //LoadQuaternions16Bit RE2
                if (MOT_HEADER.version == 78): #//LoadQuaternions13Bit RE3
                    #uint64 RotationData : 40;
                    # RotationData = readU64(f)
                    # f.seek(-3, 1); #if (SKIP) return;

                    rd = f.read(5)
                    RotationData = ((ord(rd[0]) | 0x0000000000000000) << 32) | ((ord(rd[1]) | 0x0000000000000000) << 24) | ((ord(rd[2]) | 0x0000000000000000) << 16) | ((ord(rd[3]) | 0x0000000000000000) << 8) | ((ord(rd[4]) | 0x0000000000000000) << 0)

                    self.RotationX = ((MaxUnpackX * ((RotationData >> 00) & 0x1FFF) * 0.00012208521) + MinUnpackX);
                    self.RotationY = ((MaxUnpackY * ((RotationData >> 13) & 0x1FFF) * 0.00012208521) + MinUnpackY);
                    self.RotationZ = ((MaxUnpackZ * ((RotationData >> 26) & 0x1FFF) * 0.00012208521) + MinUnpackZ);
                    self.RotationW = wRot(self);
                    return;
            if (flagsEval == 0x60000 or (MOT_HEADER.version == 65 and flagsEval == 0x50000)):             #          //LoadQuaternions16Bit RE3
                #ushort RotationDataX, RotationDataY, RotationDataZ; #if (SKIP) return;
                RotationDataX = readUShort(f)
                RotationDataY = readUShort(f)
                RotationDataZ = readUShort(f)
                self.RotationX = (MaxUnpackX * (RotationDataX / 65535.0) + MinUnpackX);
                self.RotationY = (MaxUnpackY * (RotationDataY / 65535.0) + MinUnpackY);
                self.RotationZ = (MaxUnpackZ * (RotationDataZ / 65535.0) + MinUnpackZ);
                self.RotationW = wRot(self);
                return;

            if (flagsEval == 0x70000):             #          //LoadQuaternions21Bit RE2
                if (MOT_HEADER.version == 78): #//LoadQuaternions18Bit RE3
                    #uint64 RotationData : 56;
                    # RotationData = readU64(f)
                    # f.skip(-1,1)#FSkip(-1); #if (SKIP) return;
                    rd = f.read(7)
                    RotationData = ((ord(rd[0]) | 0x0000000000000000) << 48) | ((ord(rd[1]) | 0x0000000000000000) << 40) | ((ord(rd[2]) | 0x0000000000000000) << 32) | ((ord(rd[3]) | 0x0000000000000000) << 24) | ((ord(rd[4]) | 0x0000000000000000) << 16) | ((ord(rd[5]) | 0x0000000000000000) << 8) | ((ord(rd[6]) | 0x0000000000000000) << 0)

                    self.RotationX = (MaxUnpackX * ((RotationData >> 00) & 0x1FFF) * 0.00012208521) + MinUnpackX;
                    self.RotationY = (MaxUnpackY * ((RotationData >> 13) & 0x1FFF) * 0.00012208521) + MinUnpackY;
                    self.RotationZ = (MaxUnpackZ * ((RotationData >> 26) & 0x1FFF) * 0.00012208521) + MinUnpackZ;
                    self.RotationW = wRot(self);
                    return;
            if (flagsEval == 0x80000 or (MOT_HEADER.version == 65 and flagsEval == 0x70000)):             #          //LoadQuaternions21Bit RE3
                RotationData = readU64(f);#uint64 #if (SKIP) return;
                self.RotationX = (MaxUnpackX * ((RotationData >> 00) & 0x1FFFFF) / 2097151.0) + MinUnpackX;
                self.RotationY = (MaxUnpackY * ((RotationData >> 21) & 0x1FFFFF) / 2097151.0) + MinUnpackY;
                self.RotationZ = (MaxUnpackZ * ((RotationData >> 42) & 0x1FFFFF) / 2097151.0) + MinUnpackZ;
                self.RotationW = wRot(self);
                return;

            print ("uh oh")
            # # default:
            #Printf("Unknown Rotation Type: %x at FTell %d\n", (flags & 0xFF000), FTell());

class FrameDataRot:
    def __init__(self, f, MOT, keyCount, flags, frameDataOffs, unpackDataOffs, frameIndOffs, CUR_BONE_NAME):
        start = MOT.start
        if CUR_BONE_NAME == "r_arm_radius": #and flags != 2359570:
            print (CUR_BONE_NAME)
        #uint32 keyCount, uint32 flags, uint64 frameDataOffs, uint64 unpackDataOffs, uint64 frameIndOffs
        if (frameIndOffs > 0):
            f.seek(frameIndOffs);
            self.KEYS = Keys(f, keyCount, flags, frameDataOffs)
        if (unpackDataOffs > start):
            f.seek(unpackDataOffs);

            self.unpackData = [readFloat(f),readFloat(f),readFloat(f),readFloat(f),readFloat(f),readFloat(f),readFloat(f),readFloat(f)]; #float
            MaxUnpackX = self.unpackData[0]
            MaxUnpackY = self.unpackData[1]
            MaxUnpackZ = self.unpackData[2]
            MaxUnpackW = self.unpackData[3]

            MinUnpackX = self.unpackData[4]
            MinUnpackY = self.unpackData[5]
            MinUnpackZ = self.unpackData[6]
            MinUnpackW = self.unpackData[7]
            pos2 = f.tell();
        f.seek(frameDataOffs);

        self.Frames = []
        for frame in range(0, keyCount):
            try:
                self.Frames.append(FrameRot(f, MOT, keyCount, flags, frame, self, CUR_BONE_NAME))
            except:
                print ("ROT FRAME PROBS")

        if (unpackDataOffs > start):
            f.seek(pos2);

class Tracks:
    def __init__(self, f, MOT, j):
        start = MOT.start
        MOT_HEADER = MOT.MOT_HEADER
        BONE_HEADERS = MOT.BONE_HEADERS
        BONE_CLIP_HEADERS = MOT.BONE_CLIP_HEADERS
        self.boneIdx = BONE_CLIP_HEADERS[j].boneIndex# local int boneIdx<name="Bone index"> = BONE_CLIP_HEADERS[j].boneIndex;
        # local string name <hidden=true> = "";

        self.name = BONE_CLIP_HEADERS[j].name
        self.boneHash = BONE_CLIP_HEADERS[j].boneHash

        #GET THE BONE NAME  // TODO NOT REQUIRED???
        if hasattr(BONE_HEADERS, 'BONE_HEADER'):
            for x in BONE_HEADERS.BONE_HEADER:
                if x.boneHash == self.boneHash:
                    self.name = x.boneName
                    break
        else:
            for x in MOT.MOT_LIST[boneHeadersIdx].BONE_HEADERS.BONE_HEADER:
                if x.boneHash == self.boneHash:
                    self.name = x.boneName
                    break

        self.trnsltn = False
        self.rotation = False
        self.scale = False

        TranslationFlagOff = f.tell() # local uint64 TranslationFlagOff <hidden=true> = FTell();
        if (BONE_CLIP_HEADERS[j].trackFlags & (1)): #define TRANSLATION (1)
            self.trnsltn = Track(f, MOT) #track trnsltn <name="Translation">;

        RotationFlagOff = f.tell()# local uint64 RotationFlagOff <hidden=true> = FTell();
        if (BONE_CLIP_HEADERS[j].trackFlags & (1 << 1)):
            self.rotation = Track(f, MOT) #     track rotation <name="Rotation">;

        ScaleFlagOff = f.tell()# local uint64 ScaleFlagOff <hidden=true> = FTell();
        if (BONE_CLIP_HEADERS[j].trackFlags & (1 << 2)):
            self.scale = Track(f, MOT) #     track rotation <name="Rotation">;

        pos3 = f.tell() # pos3 = FTell();


        if (BONE_CLIP_HEADERS[j].trackFlags & (1) and self.trnsltn and self.trnsltn.flags >= 0):
            f.seek(TranslationFlagOff)
            self.TranslationType = readULong(f)
            self.TranslationTypeString = get_translation_type(self.TranslationType, MOT)
        if (BONE_CLIP_HEADERS[j].trackFlags & (1 << 1) and self.rotation and self.rotation.flags >= 0):
            f.seek(RotationFlagOff)
            self.RotationType = readULong(f)#LocFrameType_t TranslationType
            self.RotationTypeString = get_rotation_type(self.RotationType, MOT)
        if (BONE_CLIP_HEADERS[j].trackFlags & (1 << 2) and self.scale and self.scale.flags >= 0):
            f.seek(ScaleFlagOff)
            self.ScaleType = readULong(f)
            self.ScaleTypeString = get_scale_type(self.ScaleType, MOT)

        if hasattr(self,"RotationTypeString" ):
            print (self.name +" : " +self.RotationTypeString)
            if hasattr(MOT,"RotationTypes" ):
                if self.RotationTypeString in MOT.RotationTypes.keys():
                    MOT.RotationTypes[self.RotationTypeString].append(self.name)
                else:
                    MOT.RotationTypes[self.RotationTypeString] = [self.name]
            else:
                MOT.RotationTypes = {}
                MOT.RotationTypes[self.RotationTypeString] = [self.name]

            #if self.RotationTypeString is "LoadQuaternionsXAxis16Bit":

        if (BONE_CLIP_HEADERS[j].trackFlags & (1)):
            if (self.trnsltn.frameIndOffs > 0):
                f.seek(self.trnsltn.frameIndOffs+start);
            else:
                f.seek(self.trnsltn.frameDataOffs+start);
            self.Frame_Data_Translation = FrameDataTrns(f, MOT ,self.trnsltn.keyCount, self.trnsltn.flags, self.trnsltn.frameDataOffs+start, self.trnsltn.unpackDataOffs+start, self.trnsltn.frameIndOffs+start)#<name="Frame Data: Translation">;
            self.Frame_Data_Translation_numFrames = self.trnsltn.keyCount
        if (BONE_CLIP_HEADERS[j].trackFlags & (1 << 1)): #if (BONE_CLIP_HEADERS[j].trackFlags & ROTATION){
            if (self.rotation.frameIndOffs > 0):
                f.seek(self.rotation.frameIndOffs+start);
            else:
                f.seek(self.rotation.frameDataOffs+start);
            self.Frame_Data_Rotation = FrameDataRot(f, MOT, self.rotation.keyCount, self.rotation.flags, self.rotation.frameDataOffs+start, self.rotation.unpackDataOffs+start, self.rotation.frameIndOffs+start, self.name)#<name="Frame Data: Rotation">;
            self.Frame_Data_Rotation_numFrames = self.rotation.keyCount
        if (BONE_CLIP_HEADERS[j].trackFlags & (1 << 2)): #BONE_CLIP_HEADERS[j].trackFlags & SCALE
            if (self.scale.frameIndOffs > 0):
                f.seek(self.scale.frameIndOffs+start);
            else:
                f.seek(self.scale.frameDataOffs+start);
            self.Frame_Data_Scale = FrameDataTrns(f, MOT, self.scale.keyCount, self.scale.flags, self.scale.frameDataOffs+start, self.scale.unpackDataOffs+start, self.scale.frameIndOffs+start)#<name="Frame Data: Scale">;
            self.Frame_Data_Scale_numFrames = self.scale.keyCount

        f.seek(pos3) # FSeek(pos3);

        # else if (exists(MOT[boneHeadersIdx].BONE_HEADERS.BONE_HEADER[boneIdx].boneName))
        #     name = MOT[boneHeadersIdx].BONE_HEADERS.BONE_HEADER[boneIdx].boneName;

class Track:
    def __init__(self, f, MOT):
        start = MOT.start
        MOT_HEADER = MOT.MOT_HEADER
        self.flags = readU32(f) #<format=binary>; //track compression among them
        self.keyCount = readU32(f)

        if (MOT_HEADER.version == 78): #//40 bytes RE2, 20 bytes RE3
            self.frameIndOffs  = readU32(f)# <format=hex>;uint32
            self.frameDataOffs = readU32(f)# <format=hex>;uint32
            self.unpackDataOffs = readU32(f)# <format=hex>uint32
        else:
            self.frameRate = readU32(f)
            self.maxFrame = readFloat(f) #float
            self.frameIndOffs = readU64(f)# <format=hex>; uint64
            self.frameDataOffs = readU64(f)# <format=hex>; uint64
            self.unpackDataOffs = readU64(f)# <format=hex>; uint64
        cmprssn = self.flags >> 20 #     local ubyte cmprssn <name="Track compression type"> = flags >> 20;
        keyFrameDataType = self.flags & 0xF00000 #     local uint keyFrameDataType <format=hex> = flags & 0xF00000;
        compression = self.flags & 0xF00000#     local uint compression <format=hex> = flags & 0xFF000;
        unkFlag = self.flags & 0xFFF#     local uint unkFlag <format=hex> = flags & 0xFFF;

class Mot:
    def __init__(self,f, MOT_LIST):
        start = f.tell()
        self.start = start
        self.MOT_LIST = MOT_LIST
        version = 99 # list version
        self.fileSize = FileSize(f)
        self.MOT_HEADER = MotHdr(f, start)

        #BONE HEADERS
        if self.MOT_HEADER.offsToBoneHdrOffs + start + 16 < self.fileSize:
            f.seek(self.MOT_HEADER.offsToBoneHdrOffs + start)
            self.BONE_HEADERS = BoneHeaders(f, start)

        #CLIP HEADERS
        f.seek(self.MOT_HEADER.boneClipHdrOffs + start)


        self.BONE_CLIP_HEADERS = []
        for i in range(0, self.MOT_HEADER.boneClipCount):
            self.BONE_CLIP_HEADERS.append(BoneClipHeader(f, self))

        skipToNextLine(f)
        #CLIP TRACKS
        #~~~~~~~~~~~~~~~~~~~
        self.CLIP_TRACKS = []
        for j in range(0, self.MOT_HEADER.boneClipCount):
            f.seek(self.BONE_CLIP_HEADERS[j].trackHdrOffs+start)
            self.CLIP_TRACKS.append(Tracks(f, self, j))   #TRACKS tracks;

        #~~~~~~~~~~~~~~~~~~~
        if ( self.MOT_HEADER.Offs1 > 0):
            f.seek(self.MOT_HEADER.Offs1 + start)
            JMAP = read_wstring(f)

        if ( self.MOT_HEADER.clipFileOffset > 0 ): #&& MOT_HEADER.version != 43
            f.seek(self.MOT_HEADER.clipFileOffset + start)
            #clip CLIP;

        # //find end of mot
        # if (bIsMotFile): ##FOR READING SINGLE MOT FILE NOT LIST
        #     f.seek( self.fileSize )
        # elif (i == numOffs-1 and GLOBAL_LIST_HEADER.POINTERS[i].Address < GLOBAL_LIST_HEADER.colOffs):
        #     f.seek(GLOBAL_LIST_HEADER.colOffs)
        # else:
        #     findEndOfMot(f)

class MotHdr:
    def __init__(self,f, start):
        self.version = readU32(f) #uint
        self.ID = f.read(4).decode("utf-8-sig") #readU32(f) # char
        self.ukn00 = readU32(f) # uint32
        self.uknOffs = readU32(f) #uint32
        self.offsToBoneHdrOffs = readU64(f)  #uint64     #BoneBaseDataPointer
        self.boneClipHdrOffs = readU64(f) #uint64 FSkip(16) = readU32(f)   #BoneDataPointer
        f.seek(16, 1)
        self.clipFileOffset = readU64(f) #uint64
        self.Offs1 =  readU64(f) # uint64
        f.seek(8, 1)
        self.Offs2 = readU64(f) #uint64
        self.namesOffs = readU64(f) #uint64           #namePointer
        self.frameCount = readFloat(f)                     #frameCount
        self.blending = readFloat(f)
        self.uknFloat = readFloat(f)
        self.uknFloat = readFloat(f)
        self.boneCount = readUShort(f) #ushort
        self.boneClipCount = readUShort(f) #ushort
        self.uknPointer2Count = readUByte(f) #ubyte
        self.uknPointer3Count = readUByte(f) # ubyte
        self.FrameRate = readUShort(f)
        self.uknPointerCount = readUShort(f)
        self.uknShort = readUShort(f)
        f.seek(self.namesOffs + start)
        self.MOT_NAME = read_wstring(f)

class Mlist:
    def __init__(self,filepath,header):
        self.filepath = filepath
        self.header = header

class ListHeader:
    def __init__(self,f):
        self.version = readU32(f)
        self.ID = f.read(4).decode("utf-8-sig")
        self.padding = readU64(f)
        self.pointersOffs = readU64(f)# uint64  pointersOffs <format=hex>; // AssetsPointer in Tyrant
        self.colOffs = readU64(f)# uint64  colOffs <format=hex>; // UnkPointer
        self.motListNameOffs = readU64(f)# uint64  motListNameOffs <format=hex>; //NamePointer
        if self.version != 60:
            self.padding = readU64(f) #uint64  padding; //UnkPointer01
        self.numOffs = readU32(f) # AssetCount
        f.seek(self.motListNameOffs)
        self.motListName = read_wstring(f)
        #pos = f.tell()

		#--gather pointers and pointer names:
        f.seek(self.pointersOffs)
        self.POINTERS = []
        for i in range(0, self.numOffs):
            self.POINTERS.append(Pointer(f))
            print (str(i) +"_"+self.POINTERS[i].motName)

def read_mot():
    #"D:\\RER_MODS\\RETool\\RE2\\re_chunk_000\\natives\\x64\\sectionroot\\cutscene\\ev\\ev040\\ev040_s00\\chara\\pl1000\\pl1000.motlist.85"
    with open("D:\\RER_MODS\\RETool\\RE2\\re_chunk_000\\natives\\x64\\sectionroot\\cutscene\\ev\\ev040\\ev040_s00\\chara\\pl1000\\pl1000.motlist.85","rb") as f:
    #with open("F:\\RE3R_MODS\\maya files\\010 anims\\em0000_es_pl_bite.motlist.99","rb") as f:

        list_header = ListHeader(f)
        GLOBAL_LIST_HEADER = list_header
        ##TODO check unique non-zero offsets
        ##LOOP OFFSETS AND GEN MOT FILE
        ##TODO check MOT version, MOT_TREE, MCAM etc. in loop

        ## TEST THIS ONE
        ##11 is loop

        MOT_LIST = []
        print(list_header.POINTERS[0].motName)
        f.seek(list_header.POINTERS[0].Address)
        MOT_LIST.append(Mot(f, MOT_LIST))

        # print(list_header.POINTERS[10].motName)
        # f.seek(list_header.POINTERS[10].Address)
        # MOT_LIST.append(Mot(f, MOT_LIST))

        re_import_mot.import_mot(MOT_LIST[0])
        #print struct.unpack("<llll",f.read(16)) #grabs one little endian 32 bit long
        f.close()

def read_mot_list(filename):
    with open(filename,"rb") as f:
        list_header = ListHeader(f)
        mlist = Mlist(filename, list_header)
        f.close()
    return mlist

def import_mot(ptr, filepath):
    with open(filepath,"rb") as f:
        list_header = ListHeader(f)
        MOT_LIST = []
        print(list_header.POINTERS[0].motName)
        f.seek(list_header.POINTERS[0].Address)
        MOT_LIST.append(Mot(f, MOT_LIST))
        f.seek(ptr.Address)
        MOT_LIST.append(Mot(f, MOT_LIST))
        re_import_mot.import_mot(MOT_LIST[1])
