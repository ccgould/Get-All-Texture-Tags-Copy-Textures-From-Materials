# Welcome to the world of Python
# Plugin\Script Developer : Ashton Rolle
# Maxon Cinema 4D Script

import c4d, os, shutil
from c4d import plugins, gui, bitmaps, documents, storage
from os import path as p

def CopyPath_To_Path(path, tex_path, pastefolder):
    if ":\\" not in path:
        # Is in tex.
        Tex_path = tex_path + "\\tex\\" + path
        shutil.copy2(Tex_path, pastefolder)
    else:
        # Not in tex.
        shutil.copy2(path, pastefolder)    
    return True

def Check_and_GetTexturePath(m_channel, tex_path, pastefolder):
    channel_shad = m_channel['shader']
    channel_text = m_channel['str']
    # Check if the (Texture....[c4d.BITMAPSHADER_FILENAME]) that it is on a bitmap.
    if not channel_shad.CheckType(c4d.Xbitmap):
        print "No bitmap apply in this channel." # Print to c4d console window. 
        pass
    else:               
        show_tex_loc_path = channel_shad[c4d.BITMAPSHADER_FILENAME]
        # Print to c4d console window. 
        print "[ " + channel_text + " Channel ]" + " / " + show_tex_loc_path
        # Copy file to the desk folder that was made and folder call ( CopyTextures ).
        CopyPath_To_Path(show_tex_loc_path, tex_path, pastefolder)
    return True

def main():
    
    # Get the user desktop to make a new folder on the desktop.
    desktop_loc = storage.GeGetC4DPath(c4d.C4D_PATH_DESKTOP)
    folder = os.path.join(desktop_loc, "C4D_CopyTextures")
    # Check if the folder exists on user desktop, if not create the folder on the user desktop.
    if not p.exists(folder):
        os.mkdir(folder)
    
    doc = c4d.documents.GetActiveDocument()
    if doc == None:
        return False
    
    # Get selected objects from the object manager.     
    list_objs = doc.GetActiveObjects(1)
    if not list_objs:
        gui.MessageDialog("Select an Object!")
        return
    
    for each_obj in list_objs:

        ProjectTexPath = doc.GetDocumentPath()
        
        # Selecting all Tags on the selected object.
        object_Tags = each_obj.GetTags()
        for each_c4d_tag  in object_Tags:
            # Checking Tag type.
            if each_c4d_tag.CheckType(c4d.Ttexture):
                
                get_t = each_c4d_tag[c4d.TEXTURETAG_MATERIAL]
                makstr = str(get_t)
                
                # Get string by spliting a long string up.
                str_1 = makstr.split("'")[1]
                finalstr = str_1.split('/')[0]
                
                # Material Name
                MatName = finalstr
                
                # Find Material
                userMat = doc.SearchMaterial(MatName)
                                
                # Get Material Shaders Texture Paths.
                if userMat[c4d.MATERIAL_USE_COLOR] == True:
                    m_color = {'str':"Color", 'shader':userMat[c4d.MATERIAL_COLOR_SHADER]}
                    Check_and_GetTexturePath(m_channel=m_color, tex_path=ProjectTexPath, pastefolder=folder)
                    
                if userMat[c4d.MATERIAL_USE_ALPHA] == True:                        
                    m_alpha = {'str':"Alpha", 'shader':userMat[c4d.MATERIAL_ALPHA_SHADER]}
                    Check_and_GetTexturePath(m_channel=m_alpha, tex_path=ProjectTexPath, pastefolder=folder)
                    
                if userMat[c4d.MATERIAL_USE_DIFFUSION] == True:    
                    m_diffusion = {'str':"Diffusion", 'shader':userMat[c4d.MATERIAL_DIFFUSION_SHADER]}
                    Check_and_GetTexturePath(m_channel=m_diffusion, tex_path=ProjectTexPath, pastefolder=folder)
                    
                if userMat[c4d.MATERIAL_USE_LUMINANCE] == True:                        
                    m_lum = {'str':"Luminance", 'shader':userMat[c4d.MATERIAL_LUMINANCE_SHADER]}
                    Check_and_GetTexturePath(m_channel=m_lum, tex_path=ProjectTexPath, pastefolder=folder)
                    
                if userMat[c4d.MATERIAL_USE_NORMAL] == True:    
                    m_nor = {'str':"Normal", 'shader':userMat[c4d.MATERIAL_NORMAL_SHADER]}
                    Check_and_GetTexturePath(m_channel=m_nor, tex_path=ProjectTexPath, pastefolder=folder)
                    
                if userMat[c4d.MATERIAL_USE_TRANSPARENCY] == True:                        
                    m_trans = {'str':"Transparency", 'shader':userMat[c4d.MATERIAL_TRANSPARENCY_SHADER]}
                    Check_and_GetTexturePath(m_channel=m_trans, tex_path=ProjectTexPath, pastefolder=folder)
                    
                if userMat[c4d.MATERIAL_USE_ENVIRONMENT] == True:                        
                    m_enviro = {'str':"Environment", 'shader':userMat[c4d.MATERIAL_ENVIRONMENT_SHADER]}
                    Check_and_GetTexturePath(m_channel=m_enviro, tex_path=ProjectTexPath, pastefolder=folder)
                    
                if userMat[c4d.MATERIAL_USE_BUMP] == True:                    
                    m_bump = {'str':"Bump", 'shader':userMat[c4d.MATERIAL_BUMP_SHADER]}
                    Check_and_GetTexturePath(m_channel=m_bump, tex_path=ProjectTexPath, pastefolder=folder)
                    
                if userMat[c4d.MATERIAL_USE_REFLECTION] == True:                
                    # To Get Reflection or Spec map texture from the Reflectance Channel of the material.
                    m_spec = userMat.GetReflectionLayerCount()
                    for each_layer in xrange(0, m_spec):  
                        layer = userMat.GetReflectionLayerIndex(each_layer)
                        get_layer_col = userMat[layer.GetDataID() + c4d.REFLECTION_LAYER_COLOR_TEXTURE]
                        get_spec = {'str':"Bump", 'shader':get_layer_col}
                        Check_and_GetTexturePath(m_channel=get_spec, tex_path=ProjectTexPath, pastefolder=folder)
                    
    c4d.EventAdd()       
                
if __name__=='__main__':
    main()
