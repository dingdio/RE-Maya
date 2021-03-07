import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import pymel.core as pm
import maya.cmds as cmds

class attrFormat:
    X = 'translateX'
    Y = 'translateY'
    Z = 'translateZ'


def import_mcam(mcam):
    cmds.currentUnit( time='ntscf' )
    name = mcam.name ##"re_camera"
    if not cmds.objExists(name):
        obj = cmds.camera(ar = 1.78, dfg= True, dr=True)
        if cmds.objExists(obj[0]) and cmds.objExists(obj[1]):
            cmds.rename(obj[1], name+"Shape")
            cmds.rename(obj[0], name)

    if hasattr(mcam.motion, 'TRANSLATE_DATA'):
        KEYS = {}
        if hasattr(mcam.motion, 'TRANSLATE_TIMES'): KEYS = mcam.motion.TRANSLATE_TIMES
        else: KEYS = [0]

        translateXFrames = []
        translateYFrames = []
        translateZFrames = []
        for frame in mcam.motion.TRANSLATE_DATA:
                translateXFrames.append(frame.x*100)
                translateYFrames.append(frame.y*100)
                translateZFrames.append(frame.z*100)

        #create re_camera if not exist??
        fill_keys(name, "translateX", KEYS, translateXFrames)
        fill_keys(name, "translateY", KEYS, translateYFrames)
        fill_keys(name, "translateZ", KEYS, translateZFrames)
        
    if hasattr(mcam.zoom, 'ZOOM_DATA'):
        KEYS = {}
        if hasattr(mcam.zoom, 'ZOOM_TIMES'): KEYS = mcam.zoom.ZOOM_TIMES
        else: KEYS = [0]
        if name == "m13_100_cam_ev01_c0390":
            pass
        zoomFrames = []
        for frame in mcam.zoom.ZOOM_DATA:
            zoomFrames.append( 100 - (frame.x *60) )

        #create re_camera if not exist??
        fill_keys(name, "fl", KEYS, zoomFrames)

    if hasattr(mcam.motion, 'ROTATE_DATA') and cmds.objExists(name):
        #~~~~~~~~~~~~~~
        cmds.select(name);
        sel_list = om.MSelectionList()
        sel_list.add(name)
        obj = sel_list.getDependNode(0)
        xform = om.MFnTransform(obj)
        #orig_rotation = xform.rotation(om.MSpace.kObject, asQuaternion=True)
        #~~~~~~~~~~~~~~
        if hasattr(mcam.motion, 'ROTATE_TIMES'): KEYS = mcam.motion.ROTATE_TIMES
        else: KEYS = [0]
        Frames = mcam.motion.ROTATE_DATA
        for (i, frame) in enumerate(Frames):
            quat = om.MQuaternion(frame.x,frame.y,frame.z,frame.w )
            quat.normalizeIt()
        #~~~~~~~~~~~~~~
        #   need to do this way to prevent gimbal problems.
            xform.setRotation(quat, om.MSpace.kObject)
            pm.setKeyframe(name, t=KEYS[i], at='rotate', minimizeRotation=True, itt='linear', ott='linear')

def import_mot(MOT):
    cmds.currentUnit( time='ntscf' )
    for clip in MOT.CLIP_TRACKS:
        name = clip.name
        if cmds.objExists(name):
            try:
                obj = cmds.listRelatives(name, ad = True)
                if obj is not None:
                    if "_parentConstraint" in obj[-1]: 
                        print (name+" has bone constraint, skipping."); continue;
            except:
                print(0)
        cmds.currentTime(0, e= 1)
        cmds.playbackOptions( min='0', max=str(MOT.MOT_HEADER.frameCount), ast='0', aet=str(MOT.MOT_HEADER.frameCount))
        if hasattr(clip, 'Frame_Data_Translation'):
            KEYS = clip.Frame_Data_Translation.KEYS.frameIndex
            Frames = clip.Frame_Data_Translation.Frames

            translateXFrames = []
            translateYFrames = []
            translateZFrames = []
            for frame in Frames:
                    translateXFrames.append(frame.X*100)
                    translateYFrames.append(frame.Y*100)
                    translateZFrames.append(frame.Z*100)
            try:
                fill_keys(name, "translateX", KEYS, translateXFrames)
                fill_keys(name, "translateY", KEYS, translateYFrames)
                fill_keys(name, "translateZ", KEYS, translateZFrames)
            except:
                print("problem adding translate keys to "+name)
        if hasattr(clip, 'Frame_Data_Rotation') and cmds.objExists(name):
            #~~~~~~~~~~~~~~
            cmds.select(name);
            sel_list = om.MSelectionList()
            sel_list.add(name)
            obj = sel_list.getDependNode(0)
            xform = om.MFnTransform(obj)
            #orig_rotation = xform.rotation(om.MSpace.kObject, asQuaternion=True)
            #~~~~~~~~~~~~~~

            KEYS = clip.Frame_Data_Rotation.KEYS.frameIndex
            Frames = clip.Frame_Data_Rotation.Frames

            rotateXFrames = []
            rotateYFrames = []
            rotateZFrames = []
            rotateWFrames = []
            for frame in Frames:
                quat = om.MQuaternion(frame.RotationX,frame.RotationY,frame.RotationZ,frame.RotationW )
                quat.normalizeIt()
            #~~~~~~~~~~~~~~
            #   need to do it this way to prevent gimbal problems. Maybe better/faster soloution in Maya API
                xform.setRotation(quat, om.MSpace.kObject)
                pm.setKeyframe(name, t=frame.Time, at='rotate', minimizeRotation=True, itt='linear', ott='linear')
            #~~~~~~~~~~~~~~
            #     if frame.inverse:
            #         quat.invertIt()
            #     euler = quat.asEulerRotation()
            #     rotateXFrames.append(euler[0] * 60)
            #     rotateYFrames.append(euler[1] * 60)
            #     rotateZFrames.append(euler[2] * 60)
            # if cmds.objExists(name):
            #     fill_keys(name, "rotateX", KEYS, rotateXFrames)
            #     fill_keys(name, "rotateY", KEYS, rotateYFrames)
            #     fill_keys(name, "rotateZ", KEYS, rotateZFrames)

        if hasattr(clip, 'Frame_Data_Scale'):
            KEYS = clip.Frame_Data_Scale.KEYS.frameIndex
            Frames = clip.Frame_Data_Scale.Frames

            scaleXFrames = []
            scaleYFrames = []
            scaleZFrames = []
            for frame in Frames:
                    scaleXFrames.append(frame.X)
                    scaleYFrames.append(frame.Y)
                    scaleZFrames.append(frame.Z)
            try:
                fill_keys(name, "scaleX", KEYS, scaleXFrames)
                fill_keys(name, "scaleY", KEYS, scaleYFrames)
                fill_keys(name, "scaleZ", KEYS, scaleZFrames)
            except:
                print("problem adding scale keys to "+name)
            ##for (i, keyframe) in enumerate(KEYS.frameIndex):
                ##pass
                #translateX
                #translateX
                #translateZ

                #print(Frames[i])
                # frame_data.Frames
                # frame_data.KEYS
    return ""

def fill_keys(name, attrName, KEYS, frameValues):
    currentObject = name
    currentAttribute = attrName
    if not cmds.objExists('%s.%s' % (currentObject, currentAttribute)):
        return


    animCurveType = 1

    # Anim Curve data
    timeList = KEYS #objectAttriData['timeList']
    valueList = frameValues #objectAttriData['valueList']


    # Convert current object and attribute to a new MPlug object
    mSelectionList = om.MSelectionList()
    mSelectionList.add('%s.%s' % (currentObject, currentAttribute))
    currentMPlug = mSelectionList.getPlug(0)

    connectedList = currentMPlug.connectedTo(1, 0)
    newAnimCurve = 1
    if connectedList :
        connectedNode = connectedList[0].node()

        if connectedNode.hasFn(om.MFn.kAnimCurve) :
            mfnAnimCurve = oma.MFnAnimCurve(connectedNode)
            newAnimCurve = 0

    if newAnimCurve == 1 :
        mfnAnimCurve = oma.MFnAnimCurve()
        mfnAnimCurve.create(currentMPlug, animCurveType)

    #mfnAnimCurve.setPreInfinityType(preInfinity)
    #mfnAnimCurve.setPostInfinityType(postInfinity)
    #mfnAnimCurve.setIsWeighted(weightedTangents)

    mTimeList = om.MTimeArray()
    mDoubleValueList = om.MDoubleArray()

    for keyIndex in range(len(timeList)) :
        mTimeList.append(om.MTime(timeList[keyIndex], om.MTime.uiUnit()))
        mDoubleValueList.append(valueList[keyIndex])

    mfnAnimCurve.addKeys(mTimeList, mDoubleValueList, 0, 0, 1)
    #cmds.filterCurve( '%s_%s' % (currentObject, currentAttribute) )
    for keyIndex in range(len(timeList)) :
        pass
        # mfnAnimCurve.setInTangentType(keyIndex, inTangentTypeList[keyIndex])
        # mfnAnimCurve.setOutTangentType(keyIndex, outTangentTypeList[keyIndex])

        # inTangentAngle = om.MAngle(inTangentAngleList[keyIndex])
        # outTangentAngle = om.MAngle(outTangentAngleList[keyIndex])

        # mfnAnimCurve.setAngle(keyIndex, inTangentAngle, 1)
        # mfnAnimCurve.setAngle(keyIndex, outTangentAngle, 0)

        # mfnAnimCurve.setWeight(keyIndex, inTangentWeightList[keyIndex], 1)
        # mfnAnimCurve.setWeight(keyIndex, outTangentWeightList[keyIndex], 0)