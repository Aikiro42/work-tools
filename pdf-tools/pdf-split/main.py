import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(pdfpath: str, outpath: str, pages: list | None = None, join: bool=False):
    # Create output folder if it doesn't exist
    os.makedirs(outpath, exist_ok=True)
    retpaths = []

    # Load the PDF
    reader = PdfReader(pdfpath)
    num_pages = len(reader.pages)

    # Determine pages to process
    pages_to_use = pages if pages is not None else list(range(1, num_pages + 1))

    if join:
        # Merge selected pages into one PDF
        writer = PdfWriter()
        for i in pages_to_use:
            writer.add_page(reader.pages[i-1])  # 1-based to 0-based index

        outfile = os.path.join(outpath, "merged.pdf")
        with open(outfile, "wb") as f:
            writer.write(f)

        retpaths.append(outfile)
        print(f"Merged {len(pages_to_use)} page{'s' if len(pages_to_use) > 1 else ''} into: {outfile}")
    else:
        # Split each page into its own PDF
        for i in range(num_pages):
            if (i+1) in pages_to_use:
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                outfile = os.path.join(outpath, f"page_{i+1:03d}.pdf")
                with open(outfile, "wb") as f:
                    writer.write(f)

                retpaths.append(outfile)

        npage = len(pages_to_use)
        print(f"Split complete! Wrote {npage} page{'s' if npage > 1 else ''} to: {outpath}")

    return retpaths

def rename_pdf(pdfpath: str, newname: str):
    # Ensure the original file exists
    if not os.path.isfile(pdfpath):
      raise FileNotFoundError(f"File not found: {pdfpath}")
    
    # Get the directory of the original PDF
    folder = os.path.dirname(pdfpath) 
    
    # Build the new full path with .pdf extension
    newpath = os.path.join(folder, f"{newname}.pdf")
    if os.path.isfile(newpath):
      print("WARNING: Renamed file exists!") 
    
    # Rename the file
    os.rename(pdfpath, newpath)

    return newpath  # Optional: return new path

All = None

if __name__ == "__main__":
  for pdfname, pages, join, renamelist in [
      # ("AL.Alvarado.EnriqueLuis.03.01-15.26", [2], False)
      # ("SALN.Alvarado.EnriqueLuis.11.16.25", [1, 2], True),
      # ("SALN.Alvarado.EnriqueLuis.12.31.25", [1, 2], True),
      # ("SALN.Alvarado.EnriqueLuis.01.05.26", [1, 2], True)
      ("CertificateMerged.Cyber.CyberSHEcurity.03.25.26", None, False, ['ABDULAZIZ I. ABDUKAHIL', 'Abegail M. Lacsena', 'ADRIENNE ALEXIS ARADO', 'AEROL CLARIZE M.  TUMOLVA', 'AICA MARIE CHANTAL V DUYAO', 'ALEXA MARIE MAMAUAG TUBIERA', 'ALEXANDRA P. TANGAN, LPT', 'Aliza Amor Nolasco', 'Aliza Mae O. Maquiñana', 'ALJEY FERNANDEZ', 'ALLYSA MEARA B. VERGARA', 'ALMIRA M. OMOSURA', 'Althea P. Caunceran', 'Ana E. Castillano', 'Angela Marie L. Lakandula', 'ANGELIE CLAIRE C GROSPE', 'Angelo Noel H. Manuel', 'Ann Loraine L. Canoy', 'Anna Cassandra B. Saberon', 'Anna Maria Sophia F. Señga', 'April Jean D. Villas', 'April Lyn Semoran Batlag', 'APRIL RHEA M. MOLINA', 'April Rose L. Pale', 'Atty. Preacious G. Gumolon', 'Banjo M. Sarturio', 'BELLIE JAY A. EDOLOVERIO', 'Bency S. Cabugsa', 'Beverly L. Patricio', 'Calayca, Ghea K.', 'CARL ALBERT N. RACOMA', 'CASSANDRA P. TUMOLVA', 'CHARRICE L MEJIA', 'CHELSEA KATE M. LIPNICA', 'Cheryll S. Santisas', 'CHRISTIAN JAYLORD S LUNANOG', 'Christian Paul O. Igbalic', 'Christian Valmoria', 'Christiansen F. Ramos', 'Christine M. Villanueva', 'Claire Anne K. Malalang', 'CLAIRE O. DEL VALLE', 'Cristine V. Mabelin', 'Cydoll Mae A. Ariban', 'DANA ANGELA V. LLORCA', 'DANICA N. MAMAUAG', 'DARLENE FAYE V. VILLASTIQUE', 'David C. Alavado', 'David J Alcarde Jr', 'Denzell Leigh Eunice Laguna', 'DIANA B. BORRAS', 'Edison S. Agaoid, MPA, CCpE', 'EDJAY L. ABARIENTOS', 'Elgin Kate N Monding', 'ELIZA F BARRIENTOS', 'Elizabeth Acab', 'ELIZAFE B. ALMAYDA', 'Ellezea A. Bautista', 'ERNEL C CALLADO', 'Euri Zebedee L. Somcio', 'Faith Lawrence T. Escano', 'FAITHE A. ULITA', 'Feliza L. Calpahi', 'FRANKY G BISMONTE', 'Franz Adriane E. Cap-atan', 'GEO RAY N GUIAO', 'GERICHO CLAUDE T. PANUGAN', 'Gie Le L Candelario', 'Gigi M. Sia', 'Gonzales, Princess M.', 'GRACE MISELIM A. BATTAD', 'GUENDAY T. GABRILLO', 'Irish Joy Noblejas', 'Jahngie G. Fabellon', 'Jamaica L. Miranda', 'JAMES A. NAVARRO', 'JAN RICH S. GEMANGA', 'JANICE L. SABAYBAY', 'JASEDINE A. BUGNOSEN', 'JAY I. PAGTALUNAN', 'JAZPER SID A. GA', 'JEANNE SHANNON O GARCIA', 'Jed Wynston L. Domingo', 'Jeff John L. Casiño', 'JEJOMAR T. DELOS TRINOS', 'JENECA R. MARIÑO', 'JENEVIEVE J. CASIL', 'JENIELYN E. SORIANO', 'JENNIFER DAGOT BERNARDINO', 'JENNIFER R CADIZ', 'JEREMY M. SILAO', 'Jeric Raye T. Bayating', 'JEROME A. CAFIRMA', 'Jerwin Carl A. Daquioag', 'JERWIN DALE D. CELETARIA', 'Jessa B. Barbacena', 'Jessiemae C. Jusayan', 'JEZRIEL L. NOVAL', 'Jhay Christian A. Edu', 'JHOECRIST A. VILLANUEVA', 'Joahnie P. Macalam', 'JOHN ALBERT A. BLANCO', 'JOHN MARC A. LUSTIVA', 'JORLEI A RODRIGUEZ', 'JOWEL C. HUELA', 'JOY KENNETH S BIASONG', 'Joy Kenneth Sala Biasong', 'JOYCE ANN C. MABALOT', 'Joycelyn Rose G. Tacusalme', 'JULINA MAE M JUNIO', 'Junesse Ednalyn E. Guevarra', 'KAREN M OSIT', 'Kassandra Crizel M. Andal', 'KATE ANGELIE M. VILLAGRACIA', 'KATHERINE M. RAVANCHO', 'KATHLEEN D. JAPITANA', 'KATHLYN N BREGUERA', 'KEITHLYNE EULA T ZONIO', 'KHRISTEL GENESE MOLINA', 'Khyle Darren A. Sibucao', 'KIER V. BASAN', 'Kimverlie Apple D. Jacinto', 'KRIS T. SARMIENTO', 'KRISHIA JANE S. DUMO', 'Kristine G. Cabungan', 'KURT ROBIN C ENOY', 'Lady Heart A. Rivera', 'LANDER RODAJE PRECILLA', 'Lazo, Jose Fernando T.', 'LEEON NATHAN S. CONSUL', 'Lei Ann T. Daez', 'LOIDA R ALNAS', 'LOU DARREN P GOROSPE', 'Lourdes Lyn B. Aquiler', 'LOVELY ROSE P. ABELO', 'LUCILLE MYSCHKIN FLORES', 'LYNIE A. VELONERO', 'Ma. Cleofe Shei S. Dacanay', 'Ma. Ellalyn A. Refil', 'MANDAC, ALLAN JOSEPH S.', 'Marc Benjie M. Sinocruz', 'Marc Ivan D. Guillermo', 'Marc Joseph B. Sacopaso', 'MARC JUSTINE P SORIANO', 'MARIA ANGELIQUE DAGOT BERNARDINO', 'MARIA CAROL B. BADIOLA', 'MARIA NIÑA ANGEL C. PINOHON', 'Mariah Golda A. Micumao-Agaoid', 'Mariane Lorraine Montoya', 'MARICEL R TIO-AN', 'Mariel I. Abreu', 'Mariel S. Rico', 'MARK JHOSUA L. LAMAN', 'Mark Joel DJ. Mapoy', 'MARK JOEL PADILLA', 'MARK JOHN C. PANGANIBAN', 'MARLENE C. BOTASTAS', 'Marlon L. Bautista, LPT', 'MARRIANE M. CEBU', 'MARY ANN D CRISOSTOMO', 'MARY ANN S. CAMARADOR', 'MARY VANESSA JANE M. LITERATO', 'Maureen P. Bautista', 'MAUREEN R. SORIANO', 'Mc Adrian M Amahoy', 'MEDELYN J. ARZADON', 'MILALYN R. MARCELO', 'Ms. Irish A. Villanueva', 'Natasha Joyfie B. Garin', 'Nica Jane S. Valencia, SO2', 'NICOLE P. BAGCAL', 'NICOLE PATRICIA V. HIPOLITO', 'Niel Alvin R. Barangan', 'NOR-ASHYA D. ABDULRAHIM', 'Norie Jane C. Morales', 'Norileen L. Himpol', 'Paul Jake G. Yuson', 'Paulette T. Espalabra', 'Pollene Joy M. De Chavez', 'Precious Liberty C. Lejao', 'PRINCE LLOYD A. DAGUIO', 'QUEEN CEL ANN P. CAPALARAN', 'QUEENEE E. GADDUANG', 'RAFAELLE JENNY F FLORES', 'RAIZA JANE O. LOTIVO', 'Ralph P. Zepeda', 'RAQUEL C. DIAL', 'RAZELLE D. ALDECOA', 'REDEN ARENA', 'REGINE A. MAPALAD', 'REX THORSTINE E. SENTINA', 'Reya E. Espiritu', 'RICHEL B. AGUISANDA', 'RODERICK F. SARMIENTO', 'Rodolfo Antonio Baltazar', 'Rogelio ll N. Lape', 'RONALD C. RAMOS', 'Ronie Pio G. Isibido', 'ROSE ANN B. ASAYTUNO', 'ROSE ANN L. BALLAD', 'ROSEMELYN MANGRUBANG VIERNES', 'RUCEL JAY M. ANDOJAR', 'RUSSEL D. DERADA', 'SAIRINE C. PREGONERO', 'Salise, Brian', 'SARAH Z MENESES', 'SEAN GABRIEL L. BERGADO', 'Shaine Dandreve P. Ascutia', 'SHAIRA CHRIZELLE ESPITA', 'SHALOM C. FEJI', 'SHAN PATRICK S. CASCAYAN', 'SHEINA ANN M. BACKONG', 'Sheryl R. Abueva', 'Shieldeen B. Millete', 'SHIRAMAE M. BARBOSA', 'SUNSHINE MAE R. VINLUAN', 'Tom Khendric S. Antig', 'VANESSA A. LUNGAN', 'WACKY P CADO', 'WINSTON RAM DAVE E. KILEM', 'ZEDECHA PORCALLA PARDIÑAS'])
  ]:
    split_pdf(f"{pdfname}.pdf", f"./split/{pdfname}", pages, join)
    if len(renamelist) <= 0:
      continue
    for i in range(len(renamelist)):
      pdfpath = f"split/{pdfname}/page_{i+1:03d}.pdf"
      rename_pdf(pdfpath, renamelist[i])
    