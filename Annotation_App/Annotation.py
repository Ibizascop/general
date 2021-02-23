# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 15:07:15 2021

@author: ibiza
"""

if __name__ == "__main__" :
    
    #Libraries
    import streamlit as st
    import pandas as pd
    from PIL import Image
    import os
    import SessionState
    import sys
    
    #Titre de l'application
    st.title("Labelisation d'images")
    
    #Récupérer données existantes si elles exi stent, sinon, initialiser un nouveau df
    #Crée une session state pour ne pas perdre les donnée à chaque changement de page
    try :
        session = SessionState.get(i= 0, get_images = False, ini = True, continued = True,
            df = pd.read_csv(sys.argv[2],sep =",",header=0)
            ,Liste_images=[],checkboxed=False)
    except (pd.errors.EmptyDataError, FileNotFoundError,IndexError) :
        session = SessionState.get(i= 0, get_images = False, continued = False,
            df = pd.DataFrame([]),Liste_images=[],checkboxed=False)
    
    #Dossier des images    
    directory = sys.argv[1]
    
    #Permet de mettre en cache les images et les
    @st.cache(allow_output_mutation=True)
    def liste_state():
        return list()
    
    
    #Crée les différentes boites où les images et boutons s'afficheront et les boutons next/stop
    placeholder_image = st.empty()
    placeholder_nvx_tags = st.empty()
    placeholder_tags_existants = st.empty()
    placeholder_tags_a_enlever = st.empty()
    placeholder_jump = st.empty()
    
    col1, col2, col3 = st.beta_columns([1,1,1])
    with col1:
        previous_button = st.button('Previous Image', key = "20")
    with col2:
        get_button = st.button('Refresh to get the tags', key = "25")                 
    with col3:
        next_button = st.button('Next Image',key ="1")
    
      
    show_button = st.sidebar.button('Show dataframe',key ="28")
    if show_button :
        st.write(session.df)
    
    number = placeholder_jump.number_input("Already treaded image number to go",min_value=0,max_value=session.df.shape[0])
    jump_button = st.sidebar.button('Go to image ',key ="48")    
    
    save_csv_button = st.sidebar.button('Save to csv',key ="2")
    save_json_button = st.sidebar.button('Save to json',key ="100")
    
    #Récupérer le nom des images
    if session.get_images == False :
        for entry in os.scandir(directory) :
            if entry.path.endswith(".jpg") or entry.path.endswith(".png") and entry.is_file() :
                session.Liste_images.append(entry.path)
        session.get_images = True
   
    #Initialisations des différents éléments
    #Initialisation des Images
    if session.continued == False :
        current_image = Image.open(session.Liste_images[session.i])
        placeholder_image.image(current_image,use_column_width=True)
    
    #Initialisation des Tags
        Liste_tags = liste_state()
        if "Notes" not in session.df.columns:
            session.df["Notes"] = 0
    
    #Si l'on avait déjà un dataframe, 
    #pour continuer travail précédent
    if session.continued == True :
        for col_a_enlever in ["Index","X","Unnamed: 0"] :
            if col_a_enlever in session.df.columns :
                session.df = session.df.drop(columns=[col_a_enlever])
        if session.ini == True :
            session.i = session.df.shape[0]-1
            session.ini = False
        current_image = Image.open(session.Liste_images[session.i])
        placeholder_image.image(current_image,use_column_width=True)
    
        
        Liste_tags = liste_state()
        for column in session.df.columns[2:] :
            if column not in Liste_tags :
                Liste_tags.append(column)
    
    
    #Récupérer les tags et la note actuelle de l'image
    tags_image = []
    for tag in session.df.columns[1:]:
            try :
                if session.df[tag].iat[session.i] == 1:
                    tags_image.append(tag)   
            except IndexError :
                pass
    st.write(tags_image)
    try :
        note = session.df["Notes"].iat[session.i]
    except IndexError :
        note = None
    #st.write(note)
    
    #Création des tags et remplir DF
    
    #Permet d'ajouter de nouveaux tags (Séparés par des virgules, sans espaces)
    tags = placeholder_nvx_tags.text_input("Nouveaux Tags de l'image",key = "4")
    
    #Permet de sélectionner parmis des tags déjà recontrés
    options = placeholder_tags_existants.multiselect('Tags déjà existants',list(Liste_tags),key = "3")
    
    tags_to_delete = placeholder_tags_a_enlever.multiselect("Tags à enlever",tags_image,key ="42")
    
    #Permet de donner une note à l'image
    if pd.isnull(note)  : 
        note = st.radio(
        "Quelle note attribuer à l'image ?",
        (1,2,3,4,5),key="10")
    #st.write(note)
    st.write('Nouveaux Tags', tags)
    st.write('You selected:', options)
    
    #Récupère les nouveaux tags et les ajoute à la liste et crée de nouvelles colones pour chaque tag
    nouveaux_tags = tags.split(",")
    for tag in nouveaux_tags :
        st.write(tag)
        if tag not in Liste_tags and tag != "" :
            Liste_tags.append(str(tag))
            session.df[tag] = 0
    
    
    #st.write(Liste_tags)
    st.write(session.i)

    #Ajoute le nom de l'image, remplit les modalités et passe à l'image suivante
    if next_button or previous_button or jump_button  :
        session.checkboxed = True
    if session.checkboxed :
        if session.i == session.df.shape[0] :
            session.df = session.df.append({"Nom.du.fichier" : session.Liste_images[session.i]},ignore_index=True)
        for tag in Liste_tags :
            if tag in options or tag in tags or tag in tags_image : 
               session.df[tag].iat[session.i] = 1
            else :
                session.df[tag].iat[session.i] = 0
        for tag in tags_to_delete :
            session.df[tag].iat[session.i] = 0
        session.df["Notes"].iat[session.i] = note
        if next_button : 
            if session.i == len(session.Liste_images)-1 :
                st.write("No following images to display")
            else :
                session.i += 1
        if previous_button :
            if session.i == 0 :
                st.write("No previous images to display")
            else :
                session.i -= 1
        if jump_button :
            session.i = number
            
        current_image = Image.open(session.Liste_images[session.i])
        placeholder_image.image(current_image,use_column_width=True)
        
     
        session.checkboxed = False
    
        
    #Enregistre le DF en csv ou json
    if save_csv_button :
        session.df = session.df[["Nom.du.fichier","Notes"] +[c for c in session.df if c not in ['Nom.du.fichier', 'Notes']]] 
        for tag in session.df.columns[2:] :
            if session.df[tag].sum() == 0 or ("Unnamed" in tag) :
                session.df = session.df.drop(columns= [tag])
        session.df.to_csv("data.txt")
       
    if save_json_button :
        session.df = session.df[["Nom.du.fichier","Notes"] +[c for c in session.df if c not in ['Nom.du.fichier', 'Notes']]] 
        
        df_final = session.df.iloc[:,[0,1]]
        df_final["Tags"] = ""
        df_final["Tags"] = df_final["Tags"].astype(object)
        for l in range(0,session.df.shape[0]-1) :
            tags_json = []
            for tag in Liste_tags :
                if session.df[tag].iat[l] == 1 :
                    tags_json.append(tag)
            df_final["Tags"].iat[l] = tags_json
        
        df_final.to_json("data.json", orient='records')
