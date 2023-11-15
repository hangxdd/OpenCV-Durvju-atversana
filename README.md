# OpenCV Durvju atvēršana
Elektromagnētisko durvju atvēršana izmantojot OpenCV un deepface sejas atpazīšanas tehnoloģiju, testa projekts.

### Kā es šo projektu varu izmēģināt?
- Clone'o šo repositery savā datorā;
- Izveido Python Virtual Environment ārpus šī projekta direktorijas;
- Aktivizē Virtual Environment;
- Projekta direktorijā ar `pip` komandu terminālī, vai sevis izvēlētajā IDE terminālī ieinstalē OpenCV un deepface priekš Python, kā arī Django un Tailwind - `pip install opencv-contrib-python`, `pip install opencv-python`, `pip install opencv-python deepface`, `pip install django`, `python -m pip install django-tailwind`;
- Tagad droši vari palaist `main.py` failu un testēt sejas atpazīšanas algoritmu!;
 _Bet iepriekš jābūt izveidotam jaunam lietotājam ar jūsu sejas bildēm lietotāju pārvaldības sistēmā, lai programma kamerā varētu jūsu seju atpazīt!_
- Lai testētu lietotāju pārvaldības mājaslapu, atver `commands.md` failu kurā vari redzēt komandas, lai palaistu Django serveri un Tailwind, pēc to izpildīšanas droši vari atvērt mājaslapu!;

### Kādēļ šis ir testa projekts?
_Šis ir testa projekts, lai tīri izprastu, kā varētu strādāt reālais risinājums izmantojot nepieciešamo elektroniku un programmēšanas tehnoloģijas, 
lai izveidotu sistēmu, kas ar sejas atpazīšanas tehnoloģiju atslēdz elektromagnētisko slēdzi durvīm un pārvaldītu sistēmā autorizētos lietotājus._

### Kāda ir šī projekta algoritma funkcionalitāte?
_Pavisam vienkārši, startējot programmu atveras neliels kameras logs un tai ir dotas 10 sekundes laiks, lai atpazītu kamerā redzamo seju ar kādu no tām, kas ir pieejamas atsauces bildēs no Amazon S3 failu servera,
ja kamera atpazīst redzamo seju, tad uz ekrāna uz brīdi ir redzams zaļš teksts "MATCH!", programma aizveras un terminālī izvada tekstu "Face found! Door's opening.", ja tā 10 sekunžu laikā
neatpazīst redzamo seju, tad programma aizveras un terminālī tiek izvadīts teksts "No matching face found..."._

### Kāda ir lietotāju pārvaldības sistēmas funkcionalitāte?
_Šī sistēma ļauj autorizētam Django administrātoram autorizēties tajā, lai pārvaldītu lietotājus kuriem ir piekļuve pie sejas atpazīšanas algoritma, lai tas tos atpazītu.
Administrators var pievienot jaunus lietotājus, sniedzot tam katram savu unikālo identifikātoru, vārdu, uzvārdu un pievienot tā bildes, kā arī dzēst un rediģēt esošos lietotājus, mainot to vārdus, uzvārdus un bildes.

### Izmantotais šajā projektā
_No programmēšanas tehnoloģijas - Visual Studio Code, Python, virtuālā vide, Django, Tailwind, OpenCV, deepface un Amazon boto3 bibliotēkas, Amazon S3 failu serveris.
No elektronikas - Iebūvētā datora kamera._

### Nepieciešamais reālajam risinājumam
_Priekš reālā risinājuma plānā būtu izmantot sekojošo elektroniku - Arduino mikrokontrolieri ar kameru, barošanas bloku un elektromagnētisko slēdzi.
Savukārt programmēšanas tehnoloģiju - Visual Studio Code, Arduino IDE, Python, virtuālo vidi, OpenCV, deepface un Amaazon boto3 bibliotēkas. <sub>**(Iespējams vel kautkas būtu nepieciešams...)**</sub>_
