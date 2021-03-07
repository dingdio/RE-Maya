from bin_helpers import (
                        read_wstring,
                        readU32,
                        readU64)

class PointerMcam:
    def __init__(self,f):
        self.Address = readU64(f)

        ##get string and return
        pos = f.tell()
        self.motName = read_wstring(f, address= self.Address + 68)
        f.seek(pos)

        if self.Address == 0:
            self.motName = ""

class Pointer:
    def __init__(self,f):
        self.Address = readU64(f)

        ##get string and return
        pos = f.tell()
        self.motName = read_wstring(f, address= self.Address + 116)
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
            if self.version == 13 or self.version == 14:
                self.POINTERS.append(PointerMcam(f))
            else:
                self.POINTERS.append(Pointer(f))
            print (str(i) +"_"+self.POINTERS[i].motName)