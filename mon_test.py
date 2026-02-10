import streamlit as st
import pandas as pd

poids = {"ch": None, "univ": None, "prives": None, "assos": None}

def poids_etab(nb_etab, voix_college, plafond=False):
	if not plafond:
		return(round(voix_college/nb_etab,2))
	else:
		if voix_college/nb_etab>pourcent_theorique:
			return(pourcent_theorique)
		else:
			return(round(voix_college/nb_etab,2))

st.logo("https://cloud.federation-flaura.fr/index.php/apps/files_sharing/publicpreview/2immTEnZ95SYyXM?file=/&fileId=12856&x=1920&y=1080&a=true&etag=5c89a8aac0b9df1959b43d0d97a16d93",
	size="large")

st.title("Simulation des votes à l'AG")

tab1, tab2, tab3 = st.tabs([":one: Réglages", ":two: Votes", ":information_source: Notice"])

with tab1:

	st.header("Nombre d'établissements par collège")
	
	col1, col2 = st.columns(2, gap="medium")
	with col1:
		nb_ch = st.slider(label="Nombre d'établissements publics ou privés à but non lucratif (ESPIC) (collège 1)", min_value=1,
			max_value=30, value=19, step=1)
		nb_prives = st.slider(label="Nombre d'établissements privés à but lucratif (collège 3)", min_value=1,
			max_value=20, value=1, step=1)

	with col2:
		nb_univ = st.slider(label="Nombre d'établissements à valence universitaire (collège 2)", min_value=1,
			max_value=6, value=5, step=1)
			
		nb_assos = st.slider(label="Nombre d'associations de personnes concernées (collège 4)", min_value=1,
			max_value=10, value=1, step=1)

	nb_total = nb_ch + nb_univ + nb_prives + nb_assos
	pourcent_theorique = round(100/nb_total, 2)

	st.write(nb_total, " établissements au total. Sans règle de pondération, chaque établissement aurait ", pourcent_theorique, "% des voix")

	st.header("Répartition des voix en pourcentage")

	col3, col4 = st.columns(2, gap="medium")

	with col3:
		st.subheader("Collège 1")
		voix_ch = st.slider(label="Pourcentage des voix accordé au collège 1", min_value=5,
			max_value=95, value=45, step=5)
		poids["ch"] = poids_etab(nb_ch, voix_ch)
		st.write("Chaque établissement de ce collège possède donc", poids["ch"], "% des voix")
		
		st.subheader("Collège 3")
		voix_prives = st.slider(label="Pourcentage des voix accordé au collège 3", min_value=5,
			max_value=95, value=10, step=5)
		plafond = st.toggle("Appliquer le plafonnement du collège 3", True)
		poids["prives"] = poids_etab(nb_prives, voix_prives, plafond)
		st.write("Chaque établissement de ce collège possède donc", poids["prives"], "% des voix")

	with col4:
		st.subheader("Collège 2")			
		voix_univ = st.slider(label="Pourcentage des voix accordé au collège 2", min_value=5,
			max_value=95, value=30, step=5)
		poids["univ"] = poids_etab(nb_univ, voix_univ)			
		st.write("Chaque établissement de ce collège possède donc", poids["univ"], "% des voix")

		st.subheader("Collège 4")
		voix_assos = st.slider(label="Pourcentage des voix accordé au collège 4", min_value=5,
			max_value=95, value=15, step=5)
		poids["assos"] = poids_etab(nb_assos, voix_assos)		
		st.write("Chaque établissement de ce collège possède donc", poids["assos"], "% des voix")
		
	voix_total = voix_ch + voix_univ + voix_prives + voix_assos

	if voix_total==100:
		st.write(":white_check_mark: Ok, le total des voix est bien égal à 100")
	else:
		st.write(":warning: Attention, le total des voix n'est pas égal à 100 : il est de ", voix_total)

with tab2:
	st.header("Répartition des votes 'Pour' par collèges")

	col5, col6 = st.columns(2, gap="medium")

	with col5:
		pour_ch = st.slider(label="Votes 'Pour' du collège 1", min_value=0,
			max_value=nb_ch, value=0, step=1)
			
		pour_prives = st.slider(label="Votes 'Pour' du collège 3", min_value=0,
			max_value=nb_prives, value=0, step=1)
	
	with col6:
		pour_univ = st.slider(label="Votes 'Pour' du collège 2", min_value=0,
			max_value=nb_univ, value=0, step=1)

		pour_assos = st.slider(label="Votes 'Pour' du collège 4", min_value=0,
			max_value=nb_assos, value=0, step=1)

	contre_ch = nb_ch - pour_ch
	contre_univ = nb_univ - pour_univ
	contre_prives = nb_prives - pour_prives
	contre_assos = nb_assos - pour_assos
	pour_total = pour_ch + pour_univ + pour_prives + pour_assos
	contre_total = contre_ch + contre_univ + contre_prives + contre_assos

	st.header("Résultats bruts")

	resultats = pd.DataFrame(
		{
			"Collège 1": [pour_ch, contre_ch],
			"Collège 2": [pour_univ, contre_univ],
			"Collège 3": [pour_prives, contre_prives],
			"Collège 4": [pour_assos, contre_assos],
		},
		index=["Pour", "Contre"],
	)
	
	resultats_table = resultats.copy()
	resultats_table["Total"] = [pour_total, contre_total]
	
	st.table(resultats_table)
	st.bar_chart(resultats)

	st.header("Résultats pondérés (exprimés en %)")

	pond_pour_ch = pour_ch * poids["ch"]
	pond_contre_ch = contre_ch * poids["ch"]
	pond_pour_univ = pour_univ * poids["univ"]
	pond_contre_univ = contre_univ * poids["univ"]
	pond_pour_prives = pour_prives * poids["prives"]
	pond_contre_prives = contre_prives * poids["prives"]
	pond_pour_assos = pour_assos * poids["assos"]
	pond_contre_assos = contre_assos * poids["assos"]
	pond_pour_total = pond_pour_ch + pond_pour_univ + pond_pour_prives + pond_pour_assos
	pond_contre_total = pond_contre_ch + pond_contre_univ + pond_contre_prives + pond_contre_assos

	resultats_ponderes = pd.DataFrame(
		{
			"Collège 1": [pond_pour_ch, pond_contre_ch],
			"Collège 2": [pond_pour_univ, pond_contre_univ],
			"Collège 3": [pond_pour_prives, pond_contre_prives],
			"Collège 4": [pond_pour_assos, pond_contre_assos],
		},
		index=["Pour", "Contre"],
	)

	resultats_ponderes_table = resultats_ponderes.copy()
	resultats_ponderes_table["Total"] = [pond_pour_total, pond_contre_total]

	st.dataframe(resultats_ponderes_table)
	st.bar_chart(resultats_ponderes)

with tab3:
	st.markdown("""
La simulation est basée sur les règles suivantes :

- Au sein d'un même collège, tous les établissements ont le même poids ;
- La logique est celle d'une expression individuelle (= par membre) pondérée
par le collège d'appartenance. Elle *n'est pas* celle d'un vote unitaire par collège ;
- Lorsque le plafonnement du collège 3 est actif (afin que le seul établissement qui
appartient à ce collège n'ait pas un poids artificiellement augmenté par la pondération de
son collège), il est normal que le total des votes ne fasse pas 100% (car le pourcentage qui est "soustrait"
n'est pas redistribué)
""")
	st.space(size="xxlarge")
	st.write("(Version 202602101111)")
