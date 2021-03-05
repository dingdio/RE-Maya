import struct
import math
import re_import_mot
reload(re_import_mot)
import pymel.core as pm
from maya import cmds

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

class McamHdr:
    def __init__(self, f, start):
        self.version = readU32(f) # uint version;
        self.ID = f.read(4).decode("utf-8-sig") # uint32 magic;
        f.seek(8, 1) #FSkip(8);
        self.motionTrackStartOffset = readU64(f);
        self.zoomStartOffset = readU64(f);
        self.thirdOffset = readU64(f);
        self.forthOffset = readU64(f);
        self.nameStringOffset = readU64(f);
        self.uknShort = readUShort(f)
        self.frameRate = readUShort(f)
        self.frameCount = readFloat(f)
        self.blending = readFloat(f)

class McamZoom:
    def __init__(self, f, start, version):
        
        if version == 14:
            ## ZOOM START
            a1 = readU32(f);
            b1 = readU32(f);

            ## ZOOM
            self.zoomHdr = TrackHeader(f)
        else:
            s = readUShort(f);
            s = readUShort(f);
            i = readU32(f);
            ukn = readU32(f);
            ukn2 = readU32(f);
            offsetStart = readU64(f);
            self.zoomHdr = TrackHeaderRE2(f)

        ## ZOOM Framelist
        if (self.zoomHdr.framesOffset > 0):
            f.seek(self.zoomHdr.framesOffset+start)
            self.ZOOM_TIMES = [readUByte(f) for _ in range(self.zoomHdr.numFrames)]

        ## ZOOM DATA
        f.seek(self.zoomHdr.dataOffset+start)
        self.ZOOM_DATA = [Vector3(f) for _ in range(self.zoomHdr.numFrames)]

class TrackHeader:
    def __init__(self, f):
        self.ukn1 = readU32(f);
        self.s1 = readUShort(f)
        self.s2 = readUShort(f);
        self.numFrames = readU32(f);
        self.framesOffset = readU32(f);
        self.dataOffset = readU32(f);

class TrackHeaderRE2:
    def __init__(self, f):
        self.zero = readU64(f);
        self.s1 = readUShort(f)
        self.s2 = readUShort(f);
        self.numFrames = readU32(f);
        self.framerate = readU32(f);
        self.endFrame = readFloat(f); #//?
        self.framesOffset = readU64(f); 
        self.dataOffset = readU64(f);


class McamMotion:
    def __init__(self, f, start, version):
        ## ROTATE AND TRANSLATE START
        if version == 14:
            a1 = readU32(f);
            b1 = readU32(f);
            self.translateHdr = TrackHeader(f)
            self.rotateHdr = TrackHeader(f)
        else:
            s = readUShort(f);
            s = readUShort(f);
            i = readU32(f);
            ukn = readU32(f);
            ukn2 = readU32(f);
            offsetStart = readU64(f);
            self.translateHdr = TrackHeaderRE2(f)
            self.rotateHdr = TrackHeaderRE2(f)

        ## TRANSLATE Framelist
        if (self.translateHdr.framesOffset > 0):
            f.seek(self.translateHdr.framesOffset+start)
            self.TRANSLATE_TIMES = [readUByte(f) for _ in range(self.translateHdr.numFrames)]

        ## TRANSLATE DATA
        f.seek(self.translateHdr.dataOffset+start)
        self.TRANSLATE_DATA = [Vector3(f) for _ in range(self.translateHdr.numFrames)]

        ## ROTATE Framelist
        if (self.rotateHdr.framesOffset > 0):
            f.seek(self.rotateHdr.framesOffset+start)
            self.ROTATE_TIMES = [readUByte(f) for _ in range(self.rotateHdr.numFrames)]

        ## ROTATE DATA
        f.seek(self.rotateHdr.dataOffset+start)
        self.ROTATE_DATA = [Quat(f) for _ in range(self.rotateHdr.numFrames)]

class Quat:
    def __init__(self,f):
        self.x = readFloat(f)
        self.y = readFloat(f)
        self.z = readFloat(f)
        self.w = readFloat(f)

class Vector3:
    def __init__(self,f):
        self.x = readFloat(f)
        self.y = readFloat(f)
        self.z = readFloat(f)


class Mcam:
    def __init__(self,f, list_header, MOT_LIST):
        start = f.tell()
        self.start = start
        self.MOT_LIST = MOT_LIST
        self.fileSize = FileSize(f)

        self.MCAM_HEADER = McamHdr(f, start)

        f.seek(self.MCAM_HEADER.nameStringOffset + start) # FSeek(offsets[4] + startof(this));
        self.name = read_wstring(f)# wstring name3;

        f.seek(self.MCAM_HEADER.motionTrackStartOffset+start)
        self.motion = McamMotion(f, start, list_header.version)


        # ZOOM CAMERA
        f.seek(self.MCAM_HEADER.zoomStartOffset+start)
        self.zoom = McamZoom(f, start, list_header.version)

        print("cake");

class PointerMcam:
    def __init__(self,f):
        self.Address = readU64(f)

        ##get string and return
        pos = f.tell()
        self.motName = read_wstring(f, address= self.Address + 68)
        f.seek(pos)

        if self.Address == 0:
            self.motName = ""

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
            self.POINTERS.append(PointerMcam(f))
            print (str(i) +"_"+self.POINTERS[i].motName)

class mcamIndex:
    def __init__(self,f):
        self.ukn1 = readU32(f)
        self.ukn2 = readU32(f)
        self.Index = readUShort(f)
        self.Switch = readUShort(f)
        self.ukn3 = readU32(f)
        self.ukn4 = readU32(f)
        self.ukn5 = readU32(f)

def read_mcam():
    with open("D:\\RER_MODS\\RETool\\DMC\\re_chunk_000\\natives\\x64\\event\\mission13\\m13_100\\motionlist\\m13_100_cam_ev01.mcamlist.13","rb") as f:
        list_header = ListHeader(f)
        MOT_LIST = []
        print(list_header.POINTERS[0].motName)

        for ptr in list_header.POINTERS:
            f.seek(ptr.Address)
            MOT_LIST.append(Mcam(f, list_header, MOT_LIST))


        mcamIndexList = []
        f.seek(list_header.colOffs) # idxOffset
        for i in range(0, list_header.numOffs):
            mcamIndexList.append(mcamIndex(f)) #mcamCount
            if cmds.objExists(MOT_LIST[i].name):
                pm.select( MOT_LIST[i].name )
                pm.cutKey( )
            re_import_mot.import_mcam(MOT_LIST[i])