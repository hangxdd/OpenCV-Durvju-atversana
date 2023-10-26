# OpenCV Durvju atvēršana
Elektromagnētisko durvju atvēršana izmantojot OpenCV un deepface sejas atpazīšanas tehnoloģiju, testa projekts.

### Kā šo projektu es varu startēt?
- Clone'o šo repositery savā datorā;
- Ar `pip` komandu sava datora terminālī, vai savā izvēlētajā IDE ieinstalē OpenCV priekš Python un deepface - `pip install opencv-contrib-python`, `pip install opencv-python`, `pip install opencv-python deepface`;
- Tagad droši vari startēt programmu un to testēt! _Bet iepriekš ar kameru uztaisi savas sejas bildi un ievieto to programmas direktorijā, lai programma tevi var atpazīt!_

### Kādēļ šis ir testa projekts?
_Šis ir testa projekts, lai tīri izprastu, kā varētu strādāt reālais risinājums izmantojot nepieciešamo elektroniku un programmēšanas tehnoloģijas, 
lai izveidotu sistēmu, kas ar sejas atpazīšanas tehnoloģiju atslēdz elektromagnētisko slēdzi durvīm._

### Kāda ir šīs programmas funkcionalitāte?
_Pavisam vienkārši, startējot programmu atveras neliels kameras logs un tai ir dotas 10 sekundes laiks, lai atpazītu kamerā redzamo seju ar kādu no tām, kas ir redzamas atsauces bildēs,
ja kamera atpazīst jūsu seju, tad uz ekrāna uz brīdi ir redzams zaļš teksts "MATCH!", programma aizveras un terminālī izvada tekstu "Face found! Door's opening.", ja tā 10 sekunžu laikā
neatpazīst redzamo seju, tad programma aizveras un terminālī tiek izvadīts teksts "No matching face found..."._

### Izmantotais šajā projektā
_No programmēšanas tehnoloģijas - Visual Studio Code, Python, virtuālā vide, OpenCV un deepface bibliotēkas.
No elektronikas - Iebūvētā datora kamera._

### Nepieciešamais reālajam risinājumam
_Priekš reālā risinājuma plānā ir izmantot sekojošo elektroniku - Arduino mikrokontrolieri ar kameru, barošanas bloku un elektromagnētisko slēdzi.
Savukārt programmēšanas tehnoloģiju - Visual Studio Code, Python, virtuālo vidi, OpenCV un deepface bibliotēkas, failu serveri priekš durvju autorizēto personu bilžu glabāšanas,
MySQL datubāzi kurā glabāsies bilžu urls, XAMPP. <sub>**(Iespējams vel kautkas turpmāk būs nepieciešams...)**</sub>_
