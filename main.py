from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os
import logging

# Logging konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

###################################################################################
# >>>>>> BU YERDA O'ZINGIZNING BOT_TOKEN NI KIRITISHNI UNUTMANG <<<<<
###################################################################################

BOT_TOKEN = "8018294597:AAEqpbRN7RU78-99TNbxr1ZCWs8R_qdvgQk"
images_paths = {
    "dish_kosashorva": r"C:\Users\kursu\Downloads\Telegram Desktop\Kosa sho'rva.jpg",
    "dish_dumbullidimlama": r"C:\Users\kursu\Downloads\Telegram Desktop\Dumbulli dimlama.jpg",
    "dish_piyozlishorva": r"C:\Users\kursu\Downloads\Telegram Desktop\Piyozli shorva.jpg",
    "dish_suyuqnorin": r"C:\Users\kursu\Downloads\Telegram Desktop\Suyuq norin.jpg",
    "dish_uygurlagmon": r"C:\Users\kursu\Downloads\Telegram Desktop\Uygur lagmon.jpg",
    "dish_moxora": r"C:\Users\kursu\Downloads\Telegram Desktop\Moxora.jpg",
    "dish_goja": r"C:\Users\kursu\Downloads\Telegram Desktop\Go'ja.jpg",
    "dish_lagmon": r"C:\Users\kursu\Downloads\Telegram Desktop\Lagmon.jpg",
    "dish_sabzavotd": r"C:\Users\kursu\Downloads\Telegram Desktop\Sabzavotli dolma.jpg",
    "dish_mantilishorva": r"C:\Users\kursu\Downloads\Telegram Desktop\Mantili shorva.jpg",
    "dish_firkadelkali": r"C:\Users\kursu\Downloads\Telegram Desktop\Firkadelkali shorva.jpg",
    "dish_kosadimlama": r"C:\Users\kursu\Downloads\Telegram Desktop\Kosa dimlama.jpg",
    "dish_tuxumdolma": r"C:\Users\kursu\Downloads\Telegram Desktop\Tuxum dolma.jpg",
    "dish_mastava": r"C:\Users\kursu\Downloads\Telegram Desktop\Mastava.jpg",
    "dish_chuchvara": r"C:\Users\kursu\Downloads\Telegram Desktop\Chuchvara.jpg",
    "dish_andijonmanti": r"C:\Users\kursu\Downloads\Telegram Desktop\Andijon manti.jpg",
    "dish_spagetti": r"C:\Users\kursu\Downloads\Telegram Desktop\Spagetti.jpg",
    "dish_qovurmala": r"C:\Users\kursu\Downloads\Telegram Desktop\Qovurma lag'mon.jpg",
    "dish_dimlama": r"C:\Users\kursu\Downloads\Telegram Desktop\Dimlama.jpg",
    "dish_beshbarmoq": r"C:\Users\kursu\Downloads\Telegram Desktop\Besh barmoq.jpg",
    "dish_bibimbap": r"C:\Users\kursu\Downloads\Telegram Desktop\Bibimbap.jpg",
    "dish_quyuqdolma": r"C:\Users\kursu\Downloads\Telegram Desktop\Do'lma.jpg",
    "dish_choyxona": r"C:\Users\kursu\Downloads\Telegram Desktop\Choyxona palov.jpg",
    "dish_gulxonim": r"C:\Users\kursu\Downloads\Telegram Desktop\Gulxonim.jpg",
    "dish_bayramona": r"C:\Users\kursu\Downloads\Telegram Desktop\Bayramona osh va ayron.jpg",
    "dish_grechkapalov": r"C:\Users\kursu\Downloads\Telegram Desktop\Grechka palov.jpg",
    "dish_turkcharatatuy": r"C:\Users\kursu\Downloads\Telegram Desktop\Turkcha ratatuy.jpg",
    "dish_balish": r"C:\Users\kursu\Downloads\Telegram Desktop\Balish.jpg",
    "dish_goshlirulet": r"C:\Users\kursu\Downloads\Telegram Desktop\Go'shli rulet.jpg",
    "dish_shivit": r"C:\Users\kursu\Downloads\Telegram Desktop\Shivit oshi.jpg",
    "dish_nonpalov": r"C:\Users\kursu\Downloads\Telegram Desktop\Non palov.jpg",
    "dish_kartoshkadolma": r"C:\Users\kursu\Downloads\Telegram Desktop\Kartoshka do'lma.jpg",
    "dish_dumbulpalov": r"C:\Users\kursu\Downloads\Telegram Desktop\Dumbul palov.jpg",
    "dish_teftel": r"C:\Users\kursu\Downloads\Telegram Desktop\Teftel.jpg",
    "dish_sarimsoqli": r"C:\Users\kursu\Downloads\Telegram Desktop\Sarimsoqli kartoshka.jpg",
    "dish_begodi": r"C:\Users\kursu\Downloads\Telegram Desktop\Begodi.jpg",
    "dish_baliqlikotlet": r"C:\Users\kursu\Downloads\Telegram Desktop\Baliqli kotlet.jpg",
    "dish_jigarkabob": r"C:\Users\kursu\Downloads\Telegram Desktop\Jigar kabob.jpg",
    "dish_qozonkabob": r"C:\Users\kursu\Downloads\Telegram Desktop\Qozon kabob.jpg",
    "dish_qiymalikabob": r"C:\Users\kursu\Downloads\Telegram Desktop\Qiymali kabob.jpg",
    "dish_tandirkabob": r"C:\Users\kursu\Downloads\Telegram Desktop\Tandir kabob.jpg",
    "dish_tovuqkabob": r"C:\Users\kursu\Downloads\Telegram Desktop\Tovuq kabob.jpg",
    "dish_namangankabob": r"C:\Users\kursu\Downloads\Telegram Desktop\Namangan kabob.jpg",
    "dish_norin": r"C:\Users\kursu\Downloads\Telegram Desktop\Norin.jpg",
    "dish_xasip": r"C:\Users\kursu\Downloads\Telegram Desktop\Xasip.jpg",
    "dish_tuxumbarak": r"C:\Users\kursu\Downloads\Telegram Desktop\Tuxum Barak.jpg",
    "dish_achchiqchuchuk": r"C:\Users\kursu\Downloads\Telegram Desktop\Achchiqchuchuksalat.jpg",
    "dish_bodringbrinza": r"C:\Users\kursu\Downloads\Telegram Desktop\Bodring va brinzali salat.jpg",
    "dish_karampomidor": r"C:\Users\kursu\Downloads\Telegram Desktop\Karam va pomidorli salat.jpg",
    "dish_gruzincha": r"C:\Users\kursu\Downloads\Telegram Desktop\Gruzincha salat.jpg",
    "dish_qarsildoq": r"C:\Users\kursu\Downloads\Telegram Desktop\Qarsildoq salat.jpg",
    "dish_suzmali": r"C:\Users\kursu\Downloads\Telegram Desktop\Suzmali salat.jpg",
    "dish_penchuza": r"C:\Users\kursu\Downloads\Telegram Desktop\Penchuza salat.jpg",
    "dish_mandarin": r"C:\Users\kursu\Downloads\Telegram Desktop\Mandarin salat.jpg",
    "dish_tovuqlisalat": r"C:\Users\kursu\Downloads\Telegram Desktop\Tovuqli salat.jpg",
    "dish_smak": r"C:\Users\kursu\Downloads\Telegram Desktop\Smak salat.jpg",
    "dish_ozdiruvchi": r"C:\Users\kursu\Downloads\Telegram Desktop\Ozdiruvchi salat.jpg",
    "dish_mevali": r"C:\Users\kursu\Downloads\Telegram Desktop\Mevali salat.jpg",
    "dish_braslet": r"C:\Users\kursu\Downloads\Telegram Desktop\Braslet salat.jpg",
    "dish_qotgannonli": r"C:\Users\kursu\Downloads\Telegram Desktop\Qotgan nonli salat.jpg",
    "dish_goshtlisa": r"C:\Users\kursu\Downloads\Telegram Desktop\Go'shtli salat.jpg",
    "dish_karamli": r"C:\Users\kursu\Downloads\Telegram Desktop\Karamli salat.jpg",
    "dish_olivye": r"C:\Users\kursu\Downloads\Telegram Desktop\Olivye.jpg",
    "dish_tovuqiolivye": r"C:\Users\kursu\Downloads\Telegram Desktop\Tovuqli olivye.jpg",
    "dish_bodringsalat": r"C:\Users\kursu\Downloads\Telegram Desktop\Bodring salat.jpg",
    "dish_shanxay": r"C:\Users\kursu\Downloads\Telegram Desktop\Shanxaycha salat.jpg",
    "dish_qushuyali": r"C:\Users\kursu\Downloads\Telegram Desktop\Qush uyali salat.jpg",
    "dish_toshkentsalat": r"C:\Users\kursu\Downloads\Telegram Desktop\Toshkentcha salat.jpg",
    "dish_portobello": r"C:\Users\kursu\Downloads\Telegram Desktop\Portobello salat.jpg",
    "dish_ananas": r"C:\Users\kursu\Downloads\Telegram Desktop\Ananas va tovuqli salat.jpg",
    "dish_sezar": r"C:\Users\kursu\Downloads\Telegram Desktop\Sezar salat.jpg",
    "dish_bodringkaram": r"C:\Users\kursu\Downloads\Telegram Desktop\Bodring va karamli salat.jpg",
    "dish_turkchaburek": r"C:\Users\kursu\Downloads\Telegram Desktop\Turkcha burek.jpg",
    "dish_goshtlisomsa": r"C:\Users\kursu\Downloads\Telegram Desktop\Go’shtli somsa.jpg",
    "dish_yupqa": r"C:\Users\kursu\Downloads\Telegram Desktop\Yupqa.jpg",
    "dish_qiymaliquymoq": r"C:\Users\kursu\Downloads\Telegram Desktop\Qiymali quymoq.jpg",
    "dish_pishloqlicheburek": r"C:\Users\kursu\Downloads\Telegram Desktop\Pishloqli cheburek.jpg",
    "dish_gumma": r"C:\Users\kursu\Downloads\Telegram Desktop\Gumma.jpg",
    "dish_pahlava": r"C:\Users\kursu\Downloads\Telegram Desktop\Pahlava.jpg",
    "dish_chakchak": r"C:\Users\kursu\Downloads\Telegram Desktop\Chak-chak.jpg",
    "dish_turkchapishiriq": r"C:\Users\kursu\Downloads\Telegram Desktop\Turkcha pishiriq.jpg",
    "dish_qozonsomsa": r"C:\Users\kursu\Downloads\Telegram Desktop\Qozon somsa.jpg",
    "dish_sabzavotlisomsa": r"C:\Users\kursu\Downloads\Telegram Desktop\Sabzavotli somsa.jpg",
    "dish_yuraksomsa": r"C:\Users\kursu\Downloads\Telegram Desktop\Yurak somsa.jpg",
    "dish_qatlamasomsa": r"C:\Users\kursu\Downloads\Telegram Desktop\Qatlama somsa.jpg",
    "dish_nisholda": r"C:\Users\kursu\Downloads\Telegram Desktop\Nisholda.jpg",
    "dish_holvetar": r"C:\Users\kursu\Downloads\Telegram Desktop\Holvetar.jpg",
    "dish_tvaroglikr": r"C:\Users\kursu\Downloads\Telegram Desktop\Tvaroglikrendel.jpg",
    "dish_shokoglazur": r"C:\Users\kursu\Downloads\Telegram Desktop\Shokoladli glazur.jpg",
    "dish_bananlieskimo": r"C:\Users\kursu\Downloads\Telegram Desktop\Bananli eskimo.jpg",
    "dish_jemlipirog": r"C:\Users\kursu\Downloads\Telegram Desktop\Jemli pirog.jpg",
    "dish_tvoroglibulochka": r"C:\Users\kursu\Downloads\Telegram Desktop\Tvaroglibulochka.jpg",
    "dish_malinalichizkeyk": r"C:\Users\kursu\Downloads\Telegram Desktop\Malinali chizkeyk.jpg",
    "dish_bolqaymoq": r"C:\Users\kursu\Downloads\Telegram Desktop\Bolqaymoq.jpg",
    "dish_murabbolipirog": r"C:\Users\kursu\Downloads\Telegram Desktop\Murabboli pirog.jpg",
    "dish_asallipirojniy": r"C:\Users\kursu\Downloads\Telegram Desktop\Asalli pirojniy.jpg",
    "dish_shaftolilimizq": r"C:\Users\kursu\Downloads\Telegram Desktop\Shaftolili muzqaymoq.jpg",
    "dish_aylanay": r"C:\Users\kursu\Downloads\Telegram Desktop\Aylanay pirogi.jpg",
    "dish_chumoliuya": r"C:\Users\kursu\Downloads\Telegram Desktop\Chumoli uyasi.jpg",
    "dish_olchali": r"C:\Users\kursu\Downloads\Telegram Desktop\Olchali pirog.jpg",
    "dish_shokokeks": r"C:\Users\kursu\Downloads\Telegram Desktop\Shokoladli keks.jpg",
    "dish_asallipechenye": r"C:\Users\kursu\Downloads\Telegram Desktop\Asalli pechenye.jpg",
    "drink_olmali": r"C:\Users\kursu\Downloads\Telegram Desktop\Olmali choy.jpg",
    "drink_namatak": r"C:\Users\kursu\Downloads\Telegram Desktop\Namatak sharbati.jpg",
    "drink_yalpizlimon": r"C:\Users\kursu\Downloads\Telegram Desktop\Yalpizli limon choy.jpg",
    "drink_qulupnay": r"C:\Users\kursu\Downloads\Telegram Desktop\Qulupnayli ichimlik.jpg",
    "drink_qovun": r"C:\Users\kursu\Downloads\Telegram Desktop\Qovun sharbati.jpg",
    "drink_bodomli": r"C:\Users\kursu\Downloads\Telegram Desktop\Bodomli sut.jpg",
    "drink_uzum": r"C:\Users\kursu\Downloads\Telegram Desktop\Uzum sharbati.jpg",
    "drink_mevali": r"C:\Users\kursu\Downloads\Telegram Desktop\Mevali sharbat.jpg",
    "drink_qatiq": r"C:\Users\kursu\Downloads\Telegram Desktop\Qatiq.jpg",
    "drink_tarvuz": r"C:\Users\kursu\Downloads\Telegram Desktop\Tarvuz sharbati.jpg",
    "drink_sabzi": r"C:\Users\kursu\Downloads\Telegram Desktop\Sabzi sharbati.jpg",
    "drink_zira": r"C:\Users\kursu\Downloads\Telegram Desktop\Zira choy.jpg",
    "drink_vitaminli": r"C:\Users\kursu\Downloads\Telegram Desktop\Vitaminli ichimlik.jpg",
    "drink_moxito": r"C:\Users\kursu\Downloads\Telegram Desktop\Moxito.jpg",
    "tort_praga": r"C:\Users\kursu\Downloads\Telegram Desktop\Praga torti.jpg",
    "tort_napaleon": r"C:\Users\kursu\Downloads\Telegram Desktop\Napaleon torti.jpg",
    "tort_zebra": r"C:\Users\kursu\Downloads\Telegram Desktop\Zebra torti.jpg",
    "tort_pancho": r"C:\Users\kursu\Downloads\Telegram Desktop\Pancho torti.jpg",
    "tort_medovik": r"C:\Users\kursu\Downloads\Telegram Desktop\Medovik torti.jpg",
    "tort_frezye": r"C:\Users\kursu\Downloads\Telegram Desktop\Frezye torti.jpg",
    "tort_karamel": r"C:\Users\kursu\Downloads\Telegram Desktop\Karamel torti.jpg",
    "tort_kitakat": r"C:\Users\kursu\Downloads\Telegram Desktop\Kita-kat torti.jpg",
    "tort_boston": r"C:\Users\kursu\Downloads\Telegram Desktop\Bostoncha kremli tort.jpg",
    "tort_bounty": r"C:\Users\kursu\Downloads\Telegram Desktop\Bounty torti.jpg",
    "tort_pavlova": r"C:\Users\kursu\Downloads\Telegram Desktop\Pavlova torti.jpg",
    "non_qatlamapatir": r"C:\Users\kursu\Downloads\Telegram Desktop\Qatlama patir.jpg",
    "non_shirinkulcha": r"C:\Users\kursu\Downloads\Telegram Desktop\Shirin kulcha.jpg",
    "non_moychechak": r"C:\Users\kursu\Downloads\Telegram Desktop\Moychechak non.jpg",
    "non_goshtli": r"C:\Users\kursu\Downloads\Telegram Desktop\Go’shtli non.jpg",
    "non_patir": r"C:\Users\kursu\Downloads\Telegram Desktop\Patir.jpg",
    "non_lochira": r"C:\Users\kursu\Downloads\Telegram Desktop\Lochira patir.jpg",
    "non_obinon": r"C:\Users\kursu\Downloads\Telegram Desktop\Obi non.jpg",
    "non_qatlama": r"C:\Users\kursu\Downloads\Telegram Desktop\Qatlama.jpg",
    "non_jizzali": r"C:\Users\kursu\Downloads\Telegram Desktop\Jizzali patir.jpg"
}

# =========================== RETSEPTLAR VA NONLAR ==============================
recipes_texts = {

    # ============= SUYUQ TAOMLAR =============
    "dish_kosashorva": """Kossa sho'rva 🥘
    Masalliqlar: 🍱

Qo‘y go‘shti - 40 g
Qo‘y qovurg‘asi - 60-70 g (1 dona)
Kichikroq kartoshka - 80-85 g (1 dona)
Sabzi - 20-30 g
Piyoz - 60-70 g
Bulg‘or qalampiri - 20 g
Sarimsoq bo‘lagi - 1 dona
Lavr bargi - 1 dona
Ivitilgan no‘xat - 1 osh qoshiq
Pomidor - 30 g
Ta’bga ko‘ra tuz, ziravorlar va ko‘katlar 

Masalliqlarni joylash: 🍱

Avval sopol ko‘zaga go‘sht va qovurg‘ani soling.
Keyin piyozdan boshqa sabzavotlarni ketma-ket joylashtiring.
Hamma masalliqlar joylangach, piyozni eng ustiga soling, shunda piyoz ezilib ketmaydi.

Qo‘shimcha yog‘:

Agar qovurga yog‘siz bo‘lsa, sho‘rvaga ta’bga ko‘ra ozgina maydalangan charvi yog‘ini qo‘shishingiz mumkin.

Suv quying:

Ko‘zani masalliqlar va suv bilan to‘ldiring.

Pishirish jarayoni: 🍱

Tayyor ko‘zani temir tandirga (duxovka) yoki elektr plitasiga qo‘ying.
Avval baland olovda, so‘ngra pastroq olovda qaynating.
Qaynash jarayonida suv kamayib qolsa, ozgina qaynagan suv qo‘shing.
Suv qaynay boshlaganda sho‘rva ko‘pigini olib tashlashni unutmang.

No‘xatni tayyorlash:

No‘xatni alohida idishda bir oz qaynatib, so‘ng sho‘rvaga qo‘shing. Bu usul sho‘rvaning tiniq va chiroyli chiqishini ta’minlaydi.

Dasturxon uchun:

Tayyor sho‘rvani kosa yoki ko‘zada mayda to‘g‘ralgan piyoz va ukrop bilan bezatib torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_dumbullidimlama": """Dumbulli dimlama🍲
    Masalliqlar: 🍱

Yog‘ – 200 g
Go‘sht – 500 g
Kartoshka – 3 ta
Sabzi – 2 ta
Piyoz – 2 ta
Bulg‘ori qalampiri – 3 ta
Pomidor – 2-3 ta
Dumbul bo‘laklari – 3 ta
Sarimsoq bo‘laklari – 2-3 ta
Ko‘kat va ziravorlar, tuz – ta’bga ko‘ra.

Masalliqlarni tayyorlash: 🍱

Go‘shtni to‘rtburchak shaklda to‘g‘rang.
Piyozni xalqasimon shaklda, kartoshkani yarim doira, sabzini doira shaklda, bulg‘orini to‘rtburchak qilib to‘g‘rang.
Pomidorni kichik to‘rtburchak shaklda, dumbullarni esa to‘rt bo‘lakka bo‘lib to‘g‘rang.
Masalliqlarni yirikroq to‘g‘rash dimlama uchun eng yaxshi tanlov.

Pishirish jarayoni: 🍱

Qozonga yog‘ni solib, qizigandan keyin go‘shtni qo‘shing.
Go‘sht qovurila boshlaganda mayda to‘g‘ralgan sarimsoqni qo‘shing va aralashtiring. Sarimsoq go‘shtga o‘zgacha ta'm beradi.
Keyin piyozni qo‘shib, yengilgina qovuring.

Masalliqlarni terish: 🍱

Piyozdan keyin qozonga qolgan masalliqlarni ketma-ket joylashtiring:
Avval sabzi, so‘ng bulg‘ori qalampiri, kartoshka.
Keyin dumbul va pomidorlarni chiroyli qilib tering.
Eng oxirida ko‘kat va ziravorlarni sepib, ta’bga ko‘ra suv quying.

Dimlash:

Qozonning qopqog‘ini yopib, taomni 40-45 daqiqa davomida dimlab qo‘ying.

Dasturxonga tortish:

Taom tayyor bo‘lgach, ta’bga ko‘ra bezatib, dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_piyozlishorva": """Piyozli sho'rva🍲
    Masalliqlar: 🍱

500 gramm mol go‘shti
700 gramm oq rangli piyoz
100 millilitr o‘simlik yog‘i
Bir nechta ko‘k piyoz shoxchalari
Ta’bga ko‘ra tuz va murch
Bir chimdim maydalangan kashnich
Bir chimdim zira.

Tayyorlash bosqichlari: 🍱

1-qadam:
Qozonda o‘simlik yog‘ini qizdiring.
Mol go‘shtini katta bo‘laklarga bo‘lib, yog‘da 4-5 daqiqa qizarguncha qovuring.
So‘ngra qozonga 200 millilitr suv quying va qopqog‘ini yopib, go‘shtni pishiring.

2-qadam:
Piyozni ingichka yarim halqa shaklida to‘g‘rang.
Go‘shtning suvi bug‘lanib ketganidan so‘ng, piyozni qozonga qo‘shing.
Go‘sht va piyozni past olovda 30 daqiqa davomida qovuring.
Eslatma: Piyoz jigarrangdan ochroq tusga kirishi kerak. Kuyib ketmasligi uchun vaqti-vaqti bilan aralashtiring.

3-qadam:
Qozonga 2 litr suv quying va ziravorlarni (zira, tuz, murch, maydalangan kashnich) soling.
Sho‘rvani o‘rtacha olovda 50-60 daqiqa davomida qaynatib pishiring.

4-qadam:
Sho‘rvani dasturxonga tortishdan oldin ko‘k piyoz bilan bezang.
Uni suxarik yoki grenkalar bilan xizmat qiling.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_suyuqnorin": """Suyuq norin🍝
    Masalliqlar: 🍱

Un – 300 g
Tuxum – 1 ta
Tuz – 15 g
Suv – 100 g
Ot go‘shti – 700 g
Qazi – 1 ta
O‘simlik yog‘i – 200-250 ml.

Tayyorlash bosqichlari: 

Xamirni tayyorlash: 🥠

Un, tuxum, suv va tuzni aralashtirib, yaxshilab xamir qoriladi.
Xamirni 20-30 daqiqa tindirib qo‘ying.

Xamirni kesish va pishirish:

Tindirilgan xamirni yupqa qilib yoyib, 15-20x20 sm hajmda to‘rtburchak shaklda kesing.
Tuz va o‘simlik yog‘i qo‘shilgan qaynayotgan suvga xamir bo‘laklarini 2-3 tadan solib pishirib oling.
Pishgan xamirlarni chovlida suzib oling va yopishib qolmasligi uchun tezroq yoyib qo‘ying.
Matoning ustiga yoyib, quriting. Xamirning har ikki tomonini quritib, so‘ng har bir bo‘lagiga o‘simlik yog‘i surtib, yassi idishga taxlang.

Xamirni to‘g‘rash:

Yog‘langan xamir bo‘laklarini eniga 4-5 smda tasma qilib kesing.
5-6 qatlam tasmani bir joyga qo‘yib, mayin qilib ugra kabi to‘g‘rang.
Xamirning mayin to‘g‘ralishi norinning chiroyi uchun muhim.

Go‘shtni tayyorlash:

Ot go‘shti va qazini tuz qo‘shib, 1-1.5 soat davomida miltillatib qaynatib pishiring.
Go‘sht va qazini suzib olib sovuting. Sho‘rvasini tashlamang – u kerak bo‘ladi.
Sovigan go‘shtni mayda to‘rtburchak shaklda to‘g‘rang (istak bo‘yicha boshqa shaklda ham bo‘lishi mumkin).

Norinni aralashtirish: 🍱

To‘g‘ralgan xamirga go‘sht, o‘simlik yog‘i va ta’bga ko‘ra yanchilgan zira qo‘shing. Hammasini birga yaxshilab aralashtiring.

Dasturxonga tortish:

Tayyorlangan norinni kosaga soling.
Go‘sht va qazi qaynatilgan sho‘rvaning tuzini rostlab, norinning ustiga quying.
Ustini parrak qilib kesilgan qazi bilan bezating.
Ta’bga ko‘ra yupqa to‘g‘ralgan piyoz va qora murch qo‘shib xizmat qilishingiz mumkin.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_uygurlagmon": """Uyg'ur lag'mon 🍜
Masalliqlar (4 kishi uchun): 🍱

300 g go‘sht
1 dona piyoz
1 osh qoshiq tomat
1/4 turp
Sabzavotlar (sabzi, bulg‘or qalampiri, baqlajon va boshqa sabzavotlar)
4 bo‘lak sarimsoq
4-5 osh qoshiq o‘simlik yog‘i
Tuz, ziravorlar
1 choy qoshiq sirka

Tayyorlash bosqichlari:

Masalliqlarni tayyorlash: 🍱
Turp va boshqa barcha sabzavotlarni ingichka qilib to‘g‘rang.

Qovurish bosqichi:
Qozonga o‘simlik yog‘ini solib, baland olovda qizdiring.
Go‘shtni qo‘shib, ozgina qovuring.
Sirka soling, olovni pasaytiring va yaxshilab aralashtiring.

Sabzavotlarni qo‘shish:
Piyozni qo‘shib qizartiring.
Keyin qolgan sabzavotlarni (sabzi, bulg‘or qalampiri va boshqalar) ketma-ket qozonga soling.

Sho‘rvani tayyorlash: 🍱
Qozonga 1,5 stakan suv quying.
Tuz va ziravorlarni qo‘shing.
Sho‘rvani 20 daqiqa davomida o‘rtacha olovda qaynatib pishiring.

Xizmat qilish:
Tayyor sho‘rvani idishga solib, issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_moxora": """Moxora🍛
Masalliqlar: 🍱

Mol go‘shti – 500 g
Kartoshka – 3 dona
Sabzi – 3 dona
Piyoz – 3 dona
Pomidor – 3 dona
No‘xat – 700 g
Achchiq qalampir – 2 dona
Tuz – ta’bga ko‘ra
Ziravorlar – ta’bga ko‘ra

Tayyorlash bosqichlari: 🍱

Go‘shtni tayyorlash:
Mol go‘shtini 30-40 g li bo‘laklarga bo‘ling.
Qozonga solib, qizartirib qovuring.

Sabzavotlarni qo‘shish:
So‘ng halqa qilib to‘g‘ralgan piyoz, kubik shaklda to‘g‘ralgan sabzi va bulg‘orini qo‘shing.
Keyin pomidorni solib, qovuring.

No‘xatni qo‘shish:
7-8 soat iliq suvda ivitilgan no‘xatni sho‘rvaga soling.
40-50 daqiqa davomida qaynatib pishiring.

Kartoshkani qo‘shish:
Kubik shaklda to‘g‘ralgan kartoshkani qo‘shing va pishguniga qadar qaynatib turing.

Ziravorlarni qo‘shish:
Ziravorlarni xohlaganingizcha suyuqlikka yoki qovurish jarayonida qo‘shishingiz mumkin.

Xizmat qilish:
Tayyor moxorani kosalarga solib, ustiga yangi ko‘katlar sepib dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_goja": """Go'ja🍲 
Masalliqlar: 🍱

Bug‘doy – 500 g
Qatiq yoki suzma (chakki) – 1,5 l
Ta’bga ko‘ra rayhon, yalpiz, qora murch va tuz

Tayyorlash bosqichlari: 🍱

Bug‘doyni tayyorlash:
Bug‘doyni yaxshilab sovuq suvda yuving.
Taxminan 3-4 litr suv qo‘shib, avval o‘rta olovda, so‘ng past olovda qaynatib pishiring. Bug‘doy yorilib pishguncha davom ettiring.

Bug‘doyni sovutish:
Pishgan bug‘doyni suzib olib, salqin joyda sovutib qo‘ying.
Agar xohlasangiz, muzlatgichga ham qo‘yishingiz mumkin, lekin bug‘doyning issiqligi chiqib, sovuganidan keyin.

Aralashtirish:
Sovigan bug‘doyni qatiq yoki suzma bilan aralashtiring.
Suv bilan bir oz suyultirib, ta’bga ko‘ra tuz va qora murch qo‘shing.

Xizmat qilish:
Tayyor bo‘lgan go‘jani sovuq holda dasturxonga torting.
Ustiga rayhon, yalpiz yoki boshqa ko‘katlar sepib bezashingiz mumkin.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_lagmon": """ Lag'mon🍝
Masalliqlar: 🍱

Un – 500 g
Tuxum – 1 dona
Suv – 180-200 ml
Tuz – yarim osh qoshiq
Go‘sht – 500 g
Piyoz – 400-500 g
Xitoy karamining qattiq joyi (basey) – 400 g
Rangli bulg‘ori qalampiri – 500-600 g
Selderey – 1-2 bog‘
O‘simlik yog‘i – 200-300 g
Pomidor – 2-3 dona
Tomat pastasi – 3-4 osh qoshiq
Sarimsoq – 1-2 bosh
Ta'bga ko‘ra ziravorlar (zira, yanchilgan kashnich urug‘i, qora murch, zanjabil, yanchilgan arpa bodiyon, yanchilgan bodiyon)

Tayyorlash bosqichlari: 🍱

1. Sabzavotlarni tayyorlash:
Piyoz, rangli bulg‘ori, pomidor, va baseylarni to‘rtburchak shaklda to‘g‘rang.
Selderey barglari va novdasini alohida to‘g‘rab, idishga solib qo‘ying.
Sarimsoqni biroz yirikroq qilib parrak-parrak to‘g‘rang.

2. Go‘shtni qovurish:
Go‘shtni yupqaroq to‘rtburchak shaklda to‘g‘rab, qizib turgan yog‘da qovuring.
Go‘sht o‘zidan suv chiqarsa, suvi tugaguncha qovuring.

3. Qaylani tayyorlash:
Go‘shtga piyoz qo‘shib, 1-2 daqiqa davomida qovuring.
Tomat pastasini qo‘shib, yana qovurishni davom eting.
So‘ng baseyni qo‘shib, 2-3 daqiqa qovuring.
Keyin bulg‘ori qalampirini solib, yana 2-3 daqiqa davomida qovuring.
Oxirida pomidor, sarimsoq va seldereyni qo‘shib, 1-2 daqiqa qovuring.
Ziravorlarni (zira, kashnich urug‘i, qora murch, zanjabil va boshqalar) solib aralashtiring.
Suv quying, suv qaynab chiqquncha kuting va tuzini rostlang.

4. Xamirni tayyorlash:
Un, tuxum, tuz va suvni idishda aralashtirib xamir qorib oling.
Xamirni tindirib, bir necha bo‘laklarga bo‘ling.
Xamirni bir necha bosqichda yog‘lash va cho‘zish usulida tayyorlang. Har bosqichda tindirib, ustini yopib qo‘yishni unutmang.
Oxirgi bosqichda xamirni stol ustiga urib cho‘zing.
Qaynab turgan suvda xamirni qaynatib oling (uzoq qaynatmang).
Qaynatilgan xamirni yog‘lab aralashtirib, bir biriga yopishib qolmasligini ta'minlang.

5. Dasturxonga tortish:
Kosaga avval xamir soling, so‘ng ustidan qayla (vaju yoki say) suzib qo‘ying.
Ustiga osh ko‘katlari bilan bezatib xizmat qiling.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_sabzavotd": """Sabzavotli dimlama🥘
Masalliqlar: 🍱

Sabzavotlar:
Bulg‘ori qalampiri – 3 ta
Kartoshka – 3 ta
Sabzi – 3 ta
Baqlajon – 3 ta
Pomidor – 2 ta

Qiymasiga:
Go‘sht – 200 g
Piyoz – 2 ta
Guruch – 150 g
Pomidor – 1 ta
Sarimsoq – 1-2 bo‘lak
Ta’bga ko‘ra tuz, ziravorlar va ko‘katlar

Tayyorlash bosqichlari: 🍱

1. Qiymaning tayyorlanishi:
Go‘shtni mayda qilib to‘g‘rang (yoki tayyor qiyma ishlating).
Piyoz, sarimsoq va ko‘katlarni mayda to‘g‘rab, pomidorni qirg‘ichdan chiqaring.
Guruchni yaxshilab yuving va hamma masalliqlarni bir idishga soling.
2-3 osh qoshiq o‘simlik yog‘i, tuz va ziravorlarni qo‘shib aralashtiring.

2. Sabzavotlarni tayyorlash:
Sabzavotlarning po‘stini archib, yaxshilab yuving.
Sabzavotlarning ichini o‘yib, tozalang. Maxsus asbob yoki oshxona pichog‘i yordamida ichini osonlikcha o‘yib olish mumkin.
Ichidan chiqqan qismini tashlamang, uni qovurishda ishlatamiz.

3. Do‘lmani to‘ldirish:
Tayyor sabzavotlarning ichini qiymadan to‘ldiring.

4. Qovurish bosqichi:
Qozonga ozroq yog‘ solib, piyozni bir-ikki marta qovuring.
Sabzavotlarning ichidan chiqqan qismini qo‘shib aralashtiring.
Qirg‘ichdan chiqarilgan pomidorni qo‘shib, 1-2 daqiqa dimlab qo‘ying.

5. Sabzavotlarni joylashtirish:
Qozonning pastki qismiga kartoshka, sabzi va bulg‘orilarni joylashtiring.
Baqlajon va pomidorlarni ustiga tering, chunki ular tez pishib ezilib ketishi mumkin.

6. Pishirish:
Qozonga suv quying va 40-45 daqiqa davomida dimlang.

7. Xizmat qilish:
Taom tayyor bo‘lgach, ta’bga ko‘ra bezating va dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_mantilishorva": """ Mantili sho'rva🥘
Masalliqlar: 🍱

Sho‘rva uchun:
Go‘sht – 200 g
Piyoz – 1 bosh
Sabzi – 2 dona
Kartoshka – 2 dona
Pomidor – 1 dona
Bulg‘ori – 1 dona
Tomat pastasi – 1 osh qoshiq
Sarimsoq – 3-4 bo‘lak
Suv – 6-7 l
O‘simlik yog‘i – 150 g
Ta'bga ko‘ra tuz va ziravorlar

Xamir uchun:
Un – 200 g (1 stakan)
Suv – 90-100 ml (yarim stakan)
Tuz – 1 choy qoshiq

Qiymasi uchun:
Go‘sht – 200 g
Piyoz – 150 g
Charvi yog‘i yoki dumba – 60-70 g
Ta'bga ko‘ra tuz va ziravorlar

Tayyorlash bosqichlari: 🍱

1. Sho‘rva tayyorlash:
Qozonda yog‘ni qizdiring.
1x1 sm to‘rtburchak shaklda to‘g‘ralgan go‘shtni solib, yaxshilab qovuring.
Piyoz, pomidor va tomat pastasini qo‘shib, qovurishda davom eting.
Masalliqlar qizg‘ish tusga kirgach, tuz va ziravorlar qo‘shing.
To‘g‘ralgan sabzi va kartoshkani qo‘shib, bir necha daqiqa qovuring.
Suv solib, qaynatishga qo‘ying.

2. Xamir tayyorlash:
Un, tuz va suvni aralashtirib, qattiq xamir qorib, 20-30 daqiqa tindiring.

3. Qiyma tayyorlash:
Go‘sht va charvi yog‘ini juda mayda qilib to‘g‘rang yoki chopib aralashtiring.
Piyozni ham mayda to‘g‘rab, qiymaga qo‘shing.
Ta'bga ko‘ra tuz va ziravor qo‘shib aralashtiring.

4. Mantilarni tugish:
Tindan xamirni yupqa qilib yoyib, 3,5-4x3,5-4 sm o‘lchamda kvadrat qilib kesing.
Har bir xamir bo‘lagiga yarim osh qoshiqdan qiyma soling.
Xamirning burchaklarini konvert shaklida yopib, ikki chetini chimchilab yopishtiring.

5. Mantilarni pishirish:
Qaynab turgan suvda mantilarni 10-12 daqiqa davomida qaynatib pishiring.
Pishgan mantilarni suzib oling.

6. Xizmat qilish:
Mantilarni kosalarga soling.
Ustiga sho‘rva quyib, osh ko‘katlari va qatiq bilan bezab dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_firkadelkali": """Firkadelkali sho'rva🍛
Masalliqlar: 🍱

500 gramm mol go'shtidan qiyma
50 gramm guruch
50 gramm bulgur
2 ta piyoz
1 ta sabzi
3 ta kartoshka
1 osh qoshiq pomidor pastasi
Ta'bga ko'ra ziravorlar
Tuz va murch – ta'bga ko'ra

Tayyorlash bosqichlari: 🍱

1. Qiymani tayyorlash:
Qiymaga bulgur, guruch va mayda to'g'ralgan piyozni qo'shing.
Tuz va murch sepib, yaxshilab aralashtiring.

2. Frikadelkalarni tayyorlash:
Qiymadan kichik dumaloq frikadelkalar yasab oling.
Frikadelkalarni unga belab, sovutgichga qo'ying.

3. Bulyon tayyorlash:
Qozonga suv soling va gazga qo'ying.
Kartoshkani bo'laklarga bo'lib, suvga qo'shing va qaynatishga qo'ying.

4. Sabzavotlarni qovurish:
Piyoz va sabzini to'rtburchak shaklda to'g'rang.
Qovurilgan piyoz va sabziga pomidor pastasi va bir oz suv qo'shib, 5 daqiqa past olovda dimlang.

5. Sho'rvaga frikadelkalarni qo'shish:
Qaynayotgan bulyonga bittadan frikadelkalarni soling.
Qopqog'ini yopib, sho'rvani 40 daqiqa davomida qaynatib pishiring.

6. Xizmat qilish:
Tayyor sho'rvani ko'katlar yoki smetana bilan bezab dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_kosadimlama": """Kosa dimlama🧆
Masalliqlar: 🍱

Go‘shtning yumshoq qismi (qo‘y go‘shti bo‘lsa yanada yaxshi) – 100-120 g
Piyoz – 1-2 ta
Kartoshka – 1-2 ta
Pomidor – 1 dona
Bulg‘ori qalampir – 1 dona
Sarimsoq – 4 bo‘lak
Ta’bga ko‘ra oshko‘kat, tuz va ziravorlar

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Kartoshka: Biroz yirik kubik shaklida to‘g‘rang.
Piyoz: Yarim halqa shaklida to‘g‘rang.
Qolgan sabzavotlar: Yirikroq bo‘laklarga bo‘ling.
Go‘sht: Yirik kubik shaklida to‘g‘rang.

2. Idishga joylashtirish:
Manty qasqonga mos keladigan kosa yoki idishga masalliqlarni navbat bilan joylashtiring:
Dastlab go‘shtni, keyin sabzavotlarni qo‘ying.
Ustidan tuz va ziravorlar sepib, tayyorlang.

3. Pishirish:
Idishni manty qasqonga joylashtiring.
Qasqonni qaynab turgan suv ustiga qo‘yib, idishni 1-1,5 soat davomida bug‘lab pishiring.

4. Xizmat qilish:
Tayyor kosa dimni ustiga oshko‘katlar sepib, dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_tuxumdolma": """Tuxum do'lma🍛
Masalliqlar: 🍱

Go‘sht (yog‘liroq qismi) – 500 g
Piyoz – 150-200 g
Charvi yoki dumba yog‘i (go‘sht yog‘siz bo‘lsa) – 100 g
Bir necha bo‘lak non
Tuxum – 1 dona (qiymaga)
Qaynatilgan tuxum – 7-8 dona
Qovurish uchun o‘simlik yog‘i
Ta'bga ko‘ra tuz va ziravorlar
(Istasangiz) 2-3 bo‘lak sarimsoq

Tayyorlash bosqichlari: 🍱

1. Qiymani tayyorlash:
Go‘sht, piyoz, non bo‘laklari va yog‘ni qiymalagichdan o‘tkazing.
Qiymaga tuz, ziravorlar va bitta tuxum solib yaxshilab aralashtiring.
Qiymani sifatli aralashtirish do‘lmalar yorilib ketmasligini ta'minlaydi.

2. Zuvalachalarni tayyorlash:
Qiymani 100-110 g bo‘laklarga bo‘lib, zuvalachalar shakllantiring.
Har bir zuvalachaning ichiga qaynatilgan tuxumni joylashtiring va ustini qiyma bilan qoplanadi.
Qiyma bo‘laklarini bir-biriga yaxshilab yopishtiring, ulangan joylarning mustahkamligiga e’tibor bering, shunda pishirish paytida ochilib ketmaydi.

3. Qovurish:
Tayyorlangan do‘lmalarni issiq yog‘da bir tekis qizarguncha qovuring.

4. Xizmat qilish:
Tayyor tuxum do‘lmalarni issiq holda dasturxonga torting. Ta'bga ko‘ra ko‘katlar yoki sous bilan bezatishingiz mumkin.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_mastava": """Mastava🍲
Masalliqlar: 🍱

Go‘sht – 300 g
Sabzi – 1-2 dona
Piyoz – 2 dona
Kartoshka – 1-2 dona
Bulg‘ori qalampiri – 1-2 dona
Sarimsoq – 5-6 bo‘lak
Guruch – 100 g
Pomidor – 1-2 dona (yoki yarim osh qoshiq tomat pastasi)
O‘simlik yog‘i – 100-150 g
Ta’bga ko‘ra tuz, ziravorlar va oshko‘katlar

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Go‘sht va sabzavotlarni (sabzi, piyoz, kartoshka, bulg‘ori qalampiri, sarimsoq) mayda kubik shaklida to‘g‘rang.

2. Go‘shtni qovurish:
Qizigan yog‘ga go‘shtni solib, 3-4 daqiqa davomida qovuring.

3. Sabzavotlarni qo‘shish:
Go‘shtga piyoz va pomidor qo‘shib, qizg‘ish tusga kirgunga qadar qovuring (pomidor o‘rniga tomat pastasi qo‘shishingiz mumkin).
Keyin sabzi, kartoshka, bulg‘ori qalampiri va sarimsoqni navbat bilan qo‘shib, qovurishda davom eting.

4. Suv va ziravorlarni qo‘shish:
Tuz va murch qo‘shib, qozonga suv quying. Mastavani qaynatishga qo‘ying.

5. Guruchni qo‘shish:
Guruchni oxirgi bosqichda, taomni dasturxonga tortiq qilishdan taxminan 10-15 daqiqa oldin qo‘shing. Bu guruchlarning dona-dona va ezilmasdan pishishini ta’minlaydi.

6. Xizmat qilish:
Tayyor mastavani kosaga suzib, ustiga osh ko‘katlar va qatiq yoki suzma solib dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_chuchvara": """Chuchvara🍲
Masalliqlar: 🍱

Qiyma – 150 g
Piyoz – 1 dona
Un – 200 g
Suv – 100 ml
Ta'bga ko‘ra tuz va ziravorlar

Tayyorlash bosqichlari: 🍱

1. Xamirni tayyorlash:
Un, suv va bir chimdim tuzni aralashtirib, qattiq xamir qoring.
Xamirni zuvala qilib, 20-30 daqiqa tindirib qo‘ying.

2. Qiymani tayyorlash:
Piyozni mayda qilib to‘g‘rang yoki choping.
Qiymaga piyoz, tuz va ziravorlarni qo‘shib yaxshilab aralashtiring.

3. Xamirni yoyish va kesish:
Tingan xamirni o‘qlov yordamida yupqa qilib yoying.
Xamirni 2x2 yoki 2,5x2,5 sm o‘lchamda to‘rtburchak shaklida kesib oling.
Kesilgan xamir bo‘laklarini quruq qolmasligi uchun yelim xaltachaga solib qo‘ying.

4. Chuchvarani tugish:
Har bir xamir bo‘lagiga choy qoshiq uchida qiyma qo‘ying.
Xamirning ikki chetini birlashtirib yopishtiring.
Keyin qiymali qatlamning ikki uchini bir-biriga yopishtirib chuchvara shakllantiring.

5. Sho‘rvani tayyorlash:
Qaynab turgan suvga yoki sho‘rvaga (suyakli qaynatma bilan) chuchvaralarni soling.
Sho‘rvaga qo‘shimcha ta'm berish uchun bir dona butun piyoz va sabzini solishingiz mumkin.

6. Chuchvarani pishirish:
Chuchvaralarni qaynab turgan sho‘rvada 10-15 daqiqa davomida qaynatib pishiring.
Sho‘rva ta’bga ko‘ra tuzlanadi.

7. Xizmat qilish:
Tayyor chuchvarani kosaga solib, ustiga qatiq qo‘shib dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    # ============= QUYUQ TAOMLAR =============

    "dish_andijonmanti": """Andijon manti🥟
Masalliqlar: 🍱

Go‘shtning yog‘li qismi – 500 g
Piyoz – 500 g
Tuxum – 1 dona
Un – 300 g
Suv yoki sut – 150 ml
Ta'bga ko‘ra tuz va ziravorlar

Tayyorlash bosqichlari: 🍱

1. Xamirni tayyorlash:
Un, suv yoki sut va tuzni aralashtirib, o‘rtacha qattiqlikda xamir qorib oling.
Xamirni 15-20 daqiqaga tindirib qo‘ying.

2. Qiymani tayyorlash:
Go‘sht va piyozni bir xil hajmdagi to‘rtburchak shaklda to‘g‘rang.
Tuxum, tuz va ziravorlarni qo‘shib yaxshilab aralashtiring.

3. Xamirni yoyish va mantini tugish:
Tindan xamirni 22-25 grammlik zuvalachalarga bo‘lib oling.
Har bir zuvalani alohida yoyib, taxminan yarim osh qoshiqdan qiyma soling.
Xamirni rasmdagi kabi o‘rtasini ochiq qoldirib, chetlarini bir-biriga yopishtirib tuging.

4. Mantini pishirish:
Tugilgan mantilarni manti qasqonga joylashtiring.
Mantilarni bug‘da 40 daqiqa davomida pishiring.

5. Xizmat qilish:
Tayyor mantilarni qatiq bilan dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_spagetti": """Spagetti🍝
Masalliqlar: 🍱

Pomidor – 4 dona
Kungaboqar yog‘i – 100 ml
Tuz – 1 choy qoshiq
Limon sharbati – 0.5 dona
Zaytun yog‘i – 4 osh qoshiq
Achchiq qizil qalampir – 1 dona
Kashnich (kinza) – 1 bog‘
Makaron (spagetti) – 500 g
Limon po‘stlog‘i – 0.5 dona

Tayyorlash bosqichlari: 🍱

1. Spagettini pishirish:
Spagettini "al dente" (biroz qattiqroq, lekin mustahkam) holatga kelguncha tuzli suvda qaynatib pishiring.
Pishgan spagettining suvini suzib oling.

2. Masalliqlarni tayyorlash:
Pomidorlarni tozalang, urug‘larini olib tashlab, kubik shaklida to‘g‘rang.
Sarimsoqni maydalang.
Kashnichni yuvib, suvini to‘kib, mayda qilib maydalang.

3. Sosni tayyorlash:
Tovaga kungaboqar yog‘ini solib qizdiring.
Maydalangan sarimsoqni qo‘shib, yengil qovuring.
Ustiga pomidor, mayda to‘g‘ralgan qalampir, va tuz qo‘shing.
10 daqiqa davomida qovuring.

4. Spagettini qo‘shish:
Tayyor sosga spagettini solib, past olovda 4 daqiqa davomida aralashtirib qovuring.

5. Xizmat qilish:
Spagettini idishga soling.
Ustiga maydalangan kashnich va limon po‘stlog‘ini sepib, taqdim eting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qovurmala": """Qovurma lag'mon🍜
Masalliqlar: 🍱

Un – 0.5 kg
Suv – 190-200 ml
Tuxum – 1 dona
Tuz – 15 g (yarim osh qoshiq)
Go‘sht – 600 g
Piyoz – 400 g
Bulg‘ori qalampiri (rangli) – 4-6 dona
Basey (xitoy karamining qattiq qismi) – 200-300 g
Pomidor – 2-3 dona
Sarimsoq – 1 bosh
Oshko‘katlar (selderey, jusey, jandiq)
O‘simlik yog‘i – 200-300 g
Tomat pastasi – 2-3 osh qoshiq
Ta'bga ko‘ra tuz va ziravorlar (zira, qora murch, arpa bodiyon, zanjabil, kashnich urug‘i va yulduzcha bodiyon)

Tayyorlash bosqichlari: 🍱

1. Xamirni tayyorlash:
Un, suv, tuxum va tuzni aralashtirib, qattiq xamir qoring.
Xamirni 20-30 daqiqa davomida tindirib qo‘ying.

2. Qayla (vaju) tayyorlash:
Go‘sht va sabzavotlarni (piyoz, bulg‘ori, basey) somon shaklida to‘g‘rang.
Baseyning barglarini ajratib, faqat qattiq qismini somon shaklida kesing.
Oshko‘kat va sarimsoqni mayda bo‘lmagan shaklda to‘g‘rang.
Qizigan yog‘ga go‘shtni solib, yaxshilab qovuring.
So‘ng piyozni qo‘shib yengilgina qovuring.
Tomat pastasini qo‘shib, aralashtiring va yana qovuring.
Basey va bulg‘ori qalampirni qo‘shib, biroz qovuring (sabzavotlar tirikroq turishi kerak).
Pomidor va oshko‘katlarni solib, 2-3 marta aralashtirib qovuring.
Eng so‘ngida ziravorlarni qo‘shib, yaxshilab aralashtirib, vaju tayyorlab qo‘ying.

3. Xamirni cho‘zish va qovurish:
Tayyor xamirni porsiyalarga bo‘lib, cho‘zib oling.
Tovaga ozroq yog‘ quyib, qizdiring.
Bir porsiya (150-170 g) xamirni tovada yengil qovuring.

4. Qovurma lag‘monni tayyorlash:
Qovurilgan xamir ustiga kerakli miqdorda qayla (vaju) soling.
Aralashtirib, yana bir oz qovuring.

5. Xizmat qilish:
Tayyor qovurma lag‘monni lagan yoki likopchaga soling.
Ustini oshko‘kat bilan bezating va xohishga ko‘ra ustiga qovurilgan tuxum qo‘shib dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_dimlama": """Dimlama🥘
Masalliqlar: 🍱

Piyoz – 200 g
Mol go‘shti – 500 g
Qizil sabzi – 150 g
Sholg‘om – 200 g
Sarimsoqpiyoz – 2 dona
Pomidor – 500 g
Kartoshka – 500 g
Makkajo‘xori – 400 g
Karam – 350-400 g
Shivit – 1 bog‘
Petrushka yoki kashnich – 1 bog‘
Ta'bga ko‘ra tuz
2 choy qoshiq zira
2 choy qoshiq quritilgan qalampir (paprika)
200 ml suv

Tayyorlash bosqichlari: 🍱

1. Sabzavotlarni tayyorlash:
Kartoshka, piyoz va sholg‘omni po‘stidandan artib, yaxshilab yuvib tayyorlang.
Kartoshkani 2 ga bo‘ling, sholg‘omni esa 1-1,5 sm qalinlikdagi halqalarga to‘g‘rang.
Piyoz va pomidorni yupqa yarim halqa shaklida to‘g‘ralang.
Makkajo‘xorini 3 yoki 4 ga bo‘ling, karamni esa 4 yoki 6 bo‘lakka kesing.

2. Go‘shtni tayyorlash:
Go‘shtni o‘rtacha bo‘laklarga bo‘lib tayyorlang.

3. Qozonda qatlamlash:
Olovni past qilib yoqing va qozonni qo‘ying.
Qozonning tagiga piyozning 1/2 qismini qo‘ying, so‘ngra go‘shtni va qolgan piyozni qo‘shing.
Ozroq tuz va zira sepib, qatlamni boshlang.
Keyin sabzi, sholg‘om, sarimsoqpiyozni soling.
Ustidan pomidorning yarmini, kartoshkani qo‘shing, paprika va tuz seping, qolgan pomidorni soling.
Qozonning yonlariga makkajo‘xorilarni joylashtirib, ustini karamlar bilan yopib, ko‘katlar soling.
Tuzi va ziravorlarni sepib, ustini yopish uchun suv qo‘shing.

4. Pishirish:
Qozon qopqog‘ini yopib, olovni balandlatib, qaynashini kuting.
Qaynab chiqqanidan so‘ng, olovni past qilib, 2 soat davomida dimlab pishiring.

5. Xizmat qilish:
Tayyor dimlamaga ko‘kat sepib, likopchaga solib dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_beshbarmoq": """Beshbarmoq🍲
Masalliqlar: 🍱

Mol go‘shti – 300 g
Piyoz – 1 dona
Un – ta'bga ko‘ra
Tuxum – 2 dona
Suv – 200 ml
Tuz – 1 choy qoshiq
Qazi – 0.5 dona

Tayyorlash bosqichlari: 🍱

1. Go‘sht va qazini tayyorlash:
Qazi va mol go‘shtini suvda pishiring.
Pishganidan so‘ng, yirik bo‘laklarga to‘g‘rang.

2. Xamirni tayyorlash:
Iliq suv, tuxum, 1 osh qoshiq yog‘, tuz va unni aralashtirib xamir qoring.
Xamirni 2 zuvalaga bo‘lib, 1 soat dam oldiring.
Tingan xamirni yupqa qilib yoyib, to‘rtburchak shaklda bo‘laklarga kesib chiqing.
Kesilgan xamir bo‘laklarini patnisga yoyib qo‘ying.

3. Sous tayyorlash:
Tovaga ozgina yog‘ soling va piyozni parrak shaklda to‘g‘rab, yengilgina qovuring.
Go‘sht qaynagan suvdan 1-2 piyola qo‘shib, qopqog‘ini yopib, 10 daqiqa past olovda dimlang.

4. Xamirni pishirish:
Go‘sht va qazi qaynagan suvda xamir bo‘laklarini 5 daqiqa davomida pishiring.

5. Dasturxonga tortish:
Laganga pishgan xamir bo‘laklarini suzib oling.
Ustiga to‘g‘ralgan go‘sht, qazi va piyozli sousni quying.
Ustiga ko‘katlar sepib, dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_bibimbap": """Bibimbap🥘
    Masalliqlar: 🍱

Mol go‘shti – 100 g
Sabzi (qizil) – 1 dona
Bodring – 1 dona
Bulg‘ori qalampiri – 1 dona
Guruch – 300 g
Tuxum – 2 dona
Sarimsoq (chesnok) – 3 dona
Ismaloq – 1 bog‘
Soya novdasi (pektin) – 200 g
Kunjut yog‘i – 3 osh qoshiq
Soya sousi – 2 osh qoshiq
Shakar – ta'bga ko‘ra
Tuz – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Guruchni pishirish:
Guruchni yuvib, multivarkada yoki an'anaviy usulda suvda qaynatib pishiring.

2. Go‘shtni marinovka qilish:
To‘g‘ralgan go‘shtga 1 choy qoshiq soya sousi, kunjut yog‘i, shakar, tuz va mayda to‘g‘ralgan sarimsoq qo‘shib, yaxshilab aralashtiring.
Go‘shtni 30 daqiqa davomida marinovkaga qo‘yib qo‘ying.

3. Sabzavotlarni tayyorlash:
Sabzi, bodring, bulg‘ori qalampirini somoncha shaklda to‘g‘rang.
Sabzi va bodringni suvi chiqib ketishi uchun ozgina tuz sepib qo‘ying.

4. Ismaloqni pishirish:
Ismaloqni yuvib, ozgina tuz va sarimsoq qo‘shib pishiring.

5. Soya novdasini tayyorlash:
Soya novdasini suvda 1-2 daqiqa qaynatib oling.
Kunjut yog‘i, sarimsoq va tuz qo‘shib aralashtiring.

6. Sabzavotlarni qovurish:
Tovaga ozroq yog‘ solib, sabzini 1 daqiqa davomida qovuring va alohida idishga soling.
Keyin bodring va bulg‘ori qalampirini ham xuddi shunday qovuring.
Qovurilgan sabzavotlarni alohida-alohida idishlarga solib qo‘ying.

7. Go‘shtni pishirish:
Marinovka qilingan go‘shtni tovada qizarguncha qovuring.

8. Tarelka yig‘ish:
Chuqurroq tarelkaga ozgina yog‘ surting.
Dastlab guruchni soling, so‘ngra pishgan sabzavotlar, ismaloq, soya novdasi va go‘shtni guruch ustiga yonma-yon terib chiqib bezating.
Yuziga qovurilgan tuxum va qalampir pastasini qo‘shing.

9. Xizmat qilish:
Tayyor bibimbapni issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""", }

# Davomi B, C, D bo‘laklarda…
# ---- KODNING DAVOMI (4-QISM, B) ----

recipes_texts.update({

    "dish_quyuqdolma": """Do'lma🥗
    Masalliqlar: 🍱

Do‘lma uchun:
Go‘sht yoki qiyma – 200 g
Piyoz – 250 g (2 bosh)
Charvi yog‘ (agar go‘sht yog‘siz bo‘lsa) – 100 g
Guruch – yarim piyola (80-100 g)
Tok yaproqlari – 25-30 dona
Ta’bga ko‘ra tuz va ziravorlar
(Ixtiyoriy) Oshko‘kat va rayhon

Qo‘shimcha masalliqlar: 🍱
Kartoshka – 1-2 dona
Sabzi – 1 dona
Piyoz – 1 dona
Bulg‘ori qalampiri – 1 dona
Pomidor – 1 dona
Sarimsoq – 5-6 bo‘lak
Ta’bga ko‘ra tuz, ziravor va oshko‘katlar
Ozroq yog‘ (sariyog‘, dumba yoki charvi yog‘i)

Tayyorlash bosqichlari: 🍱

1. Qiymaning tayyorlanishi:
Piyozni imkon boricha mayda qilib to‘g‘rang yoki choping.
Piyoz, yuvilgan guruch, go‘sht yoki qiymani aralashtirib qiyma tayyorlang.
Oshko‘kat, tuz va ziravorlarni qo‘shing.

2. Tok yaproqlarni tayyorlash:
Tok yaproqlarni qaynoq suvda 5 daqiqa davomida ivitib oling.
Barglarni suvdan olib, to‘kib qo‘ying.

3. Do‘lmalarni o‘rash:
Har bir yaproqning o‘rtasiga qiyma soling.
Pastki qismini qiymani ustiga qayirib, keyin ikki chetini ustiga qayiring.
Rulet shaklida o‘rab chiqing.

4. Qozonga terish:
Qozon tagiga kartoshka, sabzi, piyoz, bulg‘ori qalampiri, pomidor va sarimsoqni to‘g‘rab terib chiqing.
Ustiga tuz va ziravorlar seping.
Sabzavotlarning ustiga do‘lmalarni tering.

5. Yog‘ qo‘shish:
Sariyog‘ qo‘shishni istasangiz, uni do‘lmalar ustiga bo‘laklarga bo‘lib qo‘ying.
Agar dumba yoki charvi yog‘i ishlatayotgan bo‘lsangiz, uni sabzavotlar orasiga mayda kubik shaklida qo‘shing.

6. Pishirish:
Do‘lmalar ustiga 1-2 piyola suv quying.
Qozonning ustini zich yopiladigan qopqoq bilan yopib, 40 daqiqa davomida past olovda pishiring.

7. Xizmat qilish:
Tayyor do‘lmalarni laganda umumiy qilib yoki alohida likopchalarda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_choyxona": """Choyxona palov🍲
    Masalliqlar: 🍱

Qo‘y dumbasi – 400 g
Qo‘y go‘shti – 1 kg
Guruch – 1 kg
Sabzi – 1 kg (sariq bo‘lsa yaxshi, bo‘lmasa qizil)
Piyoz – 300 g
Suv
Ta’bga ko‘ra tuz va ziravorlar (zira, murch, mayiz ixtiyoriy)

Tayyorlash bosqichlari: 🍱

1. Yog‘ni eritish va jizzani tayyorlash:
Dumbani 2x2 sm kubik shaklda to‘g‘rang.
Qozonga dumbani solib, yog‘ chiqquncha va jizzasi tilla rang tusga kirguncha eritib pishiring.
Jizzani suzib oling va taomni tayyorlash davomida tanavvul qilishingiz mumkin.

2. Piyozni qovurish:
Qozondagi yog‘da yarim halqa shaklida to‘g‘ralgan piyozni qovuring.
Piyoz jigarrang tusga kirguncha qovuring, bu palovga chiroyli rang beradi.

3. Go‘shtni qovurish:
2x2 sm kubik shaklda to‘g‘ralgan go‘shtni qozonga soling.
Go‘sht suvi chiqib tugaguncha qovuring. Shu jarayonda tuz qo‘shishingiz mumkin.

4. Sabzini qo‘shish:
Sabzini somoncha shaklida to‘g‘rab, qozonga soling va 10-15 daqiqa davomida qovuring.
Bu bosqich "zirvak" deb ataladi.

5. Suv qo‘shish:
Qozonga suv qo‘shib, 5-10 daqiqa davomida qaynatib oling.
Suv qaynab chiqqach, tuzni rostlang.

6. Guruchni solish:
Iliq suvda ivitilgan guruchni qozonga avval chetidan, keyin o‘rtasidan boshlab soling.

7. Guruchni pishirish:
Guruch qaynab, bug‘langach, ohistalik bilan aralashtiring. Ustki qatlamdagi guruchni pastga, pastdagi guruchni ustga chiqaring.
Suvi tugaguncha 1-2 marta aralashtiring.

8. Dimlash:
Guruchni qozonning o‘rtasiga to‘plang.
Ustiga zira va ta’bga ko‘ra mayiz qo‘shing.
Qozonning ustini yopib, 15-20 daqiqa davomida past olovda dimlab pishiring.

9. Xizmat qilish:
Tayyor bo‘lgan palovni yaxshilab aralashtiring.
Laganga solib, ta’bga ko‘ra qazi, sarimsoq, bedana tuxumi yoki boshqa qo‘shimchalar bilan bezab dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_gulxonim": """Gulxonim
Masalliqlar: 🍱

Un – 500 g
Tuxum – 1 dona
Suv – 180-200 ml
Tuz – yarim osh qoshiq
Go‘sht (yog‘li qismi) – 300 g
Piyoz – 400 g
Kartoshka – 400 g
Agar go‘sht yog‘siz bo‘lsa: charvi yog‘ yoki o‘simlik yog‘i – 100-150 g
Ta'bga ko‘ra ziravor va tuz

Tayyorlash bosqichlari: 🍱

1. Xamirni tayyorlash:
Un, suv, tuxum va tuzni aralashtirib qattiq xamir qoring.
Xamirni ustini yopib yoki selofan paketga solib, tindirishga qo‘ying.

2. Ichki masalliqlarni tayyorlash:
Go‘sht, piyoz, kartoshkani mayda kubik shaklida to‘g‘rang.
Agar charvi yog‘i bo‘lsa, uni ham shu shaklda to‘g‘rang.
Tuz va ziravorlarni qo‘shib yaxshilab aralashtiring.
Agar o‘simlik yog‘i ishlatilsa, uni ham aralashtiring.

3. Xamirni kesish:
Tingan xamirni yupqa qilib yoying.
Xamirni eni 7-8 sm, uzunligi 18-20 sm bo‘laklarga kesib chiqing.

4. Gulxonimni tugish:
Har bir xamir bo‘lagiga qiyma qo‘ying.
Xamir bo‘lagining pastki qismini yuqoriga buklab, ikki chetini yopishtiring.
Xamirni bir chetidan o‘rab borib, oxirida ochilib ketmasligi uchun chekkasini tortib ostiga bostirib qo‘ying.

5. Pishirish:
Tayyor bo‘lgan gulxonimlarni yog‘langan manti qasqonga tering.
40-50 daqiqa davomida bug‘da pishiring.

6. Xizmat qilish:
Tayyor bo‘lgan gulxonimlarni ta'bingizga ko‘ra bezab, issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_bayramona": """Bayramona osh va ayron🍲🍶
Osh uchun masalliqlar: 🍱
Mol go‘shti (lahm) – 800 g
Qo‘y dumbasi – 200 g
Piyoz – 200 g
Sariq sabzi – 800 g
Qizil sabzi – 200 g
Guruch (“lazer”) – 1 kg
O‘simlik yog‘i – 300 ml
Osh uchun kishmish – 200 g
Ivitilgan no‘xat – 200 g
Qora murch donachalari – 1 choy qoshiq
Zira – 2 choy qoshiq
Zarchava – 1 choy qoshiq
Tuz – ta'bga ko‘ra
Toza suv – 1 l
Qaynatilgan bedana tuxumi – 10 ta

Ayron uchun masalliqlar: 🫗
Suzma – 500 g
Yalpiz (myata) – bir nechta shoxcha
Rayhon – bir nechta shoxcha
Nordon yashil olma – 200 g
Tuz – ta'bga ko‘ra
Toza suv – 300-500 ml

Tayyorlash bosqichlari: 🍱

Osh tayyorlash: ❗️

Masalliqlarni tayyorlash: 🍱
Piyozni yarim halqa, sabzini somoncha, dumba va go‘shtni katta bo‘laklarga to‘g‘rang.

Yog‘ va dumbani tayyorlash:
Qozonga yog‘ solib qizdiring. Dumbani 2-3 daqiqa davomida qizartirib qovuring va olib qo‘ying.

Go‘shtni qovurish:
Go‘sht bo‘laklarini qozonga solib, qizartirib qovuring.
Piyozni qo‘shib, yana 2-3 daqiqa davomida qovuring.

Sabzi va zirvak tayyorlash:
Qozonga sabzining 1/3 qismini solib, go‘shtni ustiga chiqarib qo‘ying.
Qolgan sabzini ham qo‘shing va qopqog‘ini yopib, past olovda 10 daqiqa pishiring.

Zirvakni pishirish:
Suv qo‘shib, kishmish, zarchava, zira, tuz va murch donachalarini soling.
Qaynab chiqqandan so‘ng, o‘rtacha olovda 40-45 daqiqa pishiring.

Guruchni tayyorlash:
Guruchni 5-6 marta yuvib, oxirida toza suv qoldirib, 1 choy qoshiq tuz soling va 20 daqiqaga bo‘ktirib qo‘ying.

Guruchni pishirish:
Zirvak ustiga dumbani joylashtiring va guruchni suvini to‘kib qozonga soling.
O‘rtacha olovda 2 daqiqa pishirib, kapkir yordamida guruchni aralashtiring.
Guruchni o‘rtaga to‘plab, zira sepib, qopqog‘ini yopib 10-15 daqiqa past olovda dimlab qo‘ying.

Xizmat qilish:
Oshni laganga suzib, ustiga bo‘laklarga kesilgan go‘sht, dumba va ikki bo‘lakka kesilgan bedana tuxumlarini joylashtiring.

Ayron tayyorlash: ❗️

Suzmaga mayda to‘g‘ralgan yalpiz, rayhon va olmani qo‘shing.
Tuz qo‘shib, suv solib yaxshilab aralashtiring.
Ayronni muzlatgichga 30 daqiqaga tinishga qo‘ying.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_grechkapalov": """Grechka palov🍲
Masalliqlar: 🍱

Mol go‘shti – 200-300 g
Kartoshka – 2 dona
Sabzi – 3 dona
Piyoz – 1 dona
Pomidor – 1 dona (yoki tomat sousi)
Kungaboqar yog‘i – ta'bga ko‘ra
Tuz – ta'bga ko‘ra
Grechka – 500 g

Tayyorlash bosqichlari: 🍱

Masalliqlarni tayyorlash: 🍱
Go‘sht va kartoshkani yirik kubik shaklda, sabzini somoncha shaklda to‘g‘rang.
Piyozni yarim halqa yoki parrak shaklda kesib oling.

Qovurish:
Qozonga 1 cho‘mich yog‘ solib qizdiring.
Piyozni qo‘shib, yengil qizartiring.
Keyin go‘shtni solib, qizarguncha qovuring.
Sabzi va kartoshkani qo‘shib, aralashtirib, birga qovuring.

Pomidor va zirvak tayyorlash:
Pomidor yoki tomat sousini qo‘shib, aralashtiring.
Ta'bga ko‘ra tuz qo‘shing va qovurishda davom eting.
Qozonga suv quying va qaynab chiqqandan so‘ng, olovni pasaytirib, 30-40 daqiqa davomida qaynatib pishiring.

Grechka qo‘shish:
Grechka yormasini tozalab, yaxshilab yuving.
Uni qozonga soling, zirvak suvi grechkani to‘liq yopishi kerak.
Suvi tortilib qolgach, grechkani qozon o‘rtasiga uyib joylashtiring.

Damlash:
Qozon qopqog‘ini yopib, 20 daqiqa davomida past olovda damlang.

Xizmat qilish:
Tayyor grechka palovni likopchalarga suzib, ustiga ko‘kat sepib dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_turkcharatatuy": """Turkcha ratatuy🥘
Masalliqlar: 🍱

Qovoqcha – 2 dona
Baqlajon – 2 dona
Pomidor – 4 dona
Rangli bulg‘ori qalampiri – 1 tadan
Sarimsoq – 3 tish
Mol go‘shtidan qiyma – 500 g
O‘simlik yog‘i – 1 osh qoshiq
Oregano – 0,5 choy qoshiq
Tuz va murch – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

Qiymani tayyorlash:
Qiymaga tuz va murch qo‘shib, yaxshilab aralashtiring.

Sabzavotlarni to‘g‘rash:
Baqlajon, qovoqcha, bulg‘ori qalampiri va 2-3 ta pomidorni 1 sm qalinlikda parrak qilib to‘g‘rang.

Kotletchalar tayyorlash:
Qiymadan sabzavotlarning kattaligi va qalinligida kichik kotletchalar yasang.

Qolipni tayyorlash:
Dumaloq yoki to‘rtburchak shakldagi qolipni o‘simlik yog‘i bilan yog‘lang.
Kotletlar va sabzavotlarni istalgan ketma-ketlikda qolipga joylashtiring.

Qayla tayyorlash:
Blenderda qolgan pomidor va sarimsoqni maydalang.
Ta'bga ko‘ra tuz va oregano qo‘shing.
Hosil bo‘lgan qaylani qolipdagi sabzavotlar va kotletchalar ustidan quying.

Pishirish:
Ratatuyni 180°C darajada qizdirilgan gaz pechida 40-45 daqiqa davomida pishiring.

7. Xizmat qilish:
Tayyor ratatuyni issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_balish": """Balish🧆
Masalliqlar: 🍱

Kartoshka – 1-2 dona
Piyoz – 1-2 dona
Bulg‘ori qalampiri (qizil va yashil) – 2 dona
Pomidor – 1 dona
Yog‘ (istalgan o‘simlik moyi, charvi, dumba yoki sariyog‘) – ta'bga ko‘ra
Un – 1 kg
Tuz – 1 osh qoshiq
Sut – 600 ml
Xamirturush (droja) – 10 g
Ta'bga ko‘ra tuz, ziravor va oshko‘katlar

Tayyorlash bosqichlari: 🍱

1. Xamirni tayyorlash:
Sutni iliq holga keltiring va unga xamirturush, tuz qo‘shib yaxshilab aralashtiring.
Yumshoq xamir qorib, ustini yopib 1 soatga oshishga qo‘yib qo‘ying.

2. Qaylani tayyorlash:
Kartoshka, piyoz, bulg‘ori qalampiri va pomidorni mayda kubik shaklda to‘g‘rang.
Ta'bga ko‘ra tuz, ziravor va oshko‘katlar qo‘shib aralashtiring.
Yog‘ni ham qo‘shib yaxshilab aralashtiring.
Agar xohlasangiz, bir necha balishni go‘shtli qilish uchun mayda to‘g‘ralgan go‘sht qo‘shishingiz mumkin.

3. Xamirni bo‘lish va yoyish:
Oshgan xamirni 50-60 grammlik zuvalachalarga bo‘lib oling va 10 daqiqa tindiring.
Zuvalachalarni juva yordamida yoyib chiqing.

4. Balishni tugish:
Har bir yoyilgan xamirning o‘rtasiga tayyor qayladan qo‘ying.
Xamirning chetlarini Andijon manti kabi bir chetidan ustma-ust yopishtirib tuging.

5. Pishirish:
Tugilgan balishlarning ustiga tuxum surtib, avvaldan 200°C darajaga qizdirilgan dimxonada 20-30 daqiqa davomida pishiring.

6. Xizmat qilish:
Tayyor bo‘lgan balishlarni issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_goshlirulet": """Go'shtli rulet🍣
Masalliqlar: 🍱

Mol go‘shti – 1 kg
Piyoz – 1 dona
Tuxum – 2 dona
Tuz – ta'bga ko‘ra
Tuyilgan qora murch – ta'bga ko‘ra
Tomat pastasi – 400 ml
Pishloq – 200 g
Sarimsoq – 2 dona
Nami qochgan non – 3 osh qoshiq

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Piyozni halqa shaklida kesib oling.
Sarimsoqpiyozni mayda qirg‘ichdan chiqaring.

2. Nachinka tayyorlash:
Bir idishda sarimsoqpiyoz, urvoq, rayhon, oregano, petrushka va tuzni aralashtiring.
Tuxum va qirg‘ichdan o‘tkazilgan pishloqni qo‘shib yaxshilab aralashtiring.

3. Go‘shtni tayyorlash:
Go‘shtni tolalari bo‘ylab ochib kesing (oxirigacha kesmang).
Go‘shtning qalinligi 1 sm dan oshmasligi lozim.
Tuz va murch seping.

4. Ruletni shakllantirish:
Tayyorlangan nachinkani go‘shtning ustiga bir tekis surting, lekin bir chetida 2 sm bo‘sh joy qoldiring.
Go‘shtni ehtiyotkorlik bilan rulet shaklida o‘rang.

5. Ruletni bog‘lash:
Ruletni ip yordamida mahkam bog‘lang.

6. Pishirish:
Tovaga piyoz halqalarini joylashtiring, ustiga ruletni qo‘ying (choki pastga qaragan bo‘lsin).
Tomat pastasini ruletning ustidan quying.
Tovani folga bilan yopib, oldindan 180°C darajaga qizdirilgan duxovkaga joylashtiring.
Ruletni 2 soat davomida pishiring.

7. Ustini qizartirish:
Pishirishning oxirida (so‘nggi 20 daqiqa) folgani olib, ruletning usti qizartib pishishini ta'minlang.

8. Xizmat qilish:
Tayyor ruletni dilimlab, issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_shivit": """Shivit oshi🍛
Masalliqlar: 🍱

Xamir uchun:
Shivit (ukrop) – 2 bog‘
Suv – 200 ml
Tuxum – 1 dona
Tuz – 1 choy qoshiq
Un – 650-700 g

Vaju uchun:
Mol go‘shti – 500 g
Pomidor – 200 g
Sabzi – 200 g
Piyoz – 150 g
Kartoshka – 150 g
Qizil bulg‘ori qalampiri – 200 g
Sarimsoq – 3 dona
Pomidor pastasi – 2 osh qoshiq
O‘simlik yog‘i – 50 ml
Zira – ta'bga ko‘ra
Tuz va murch – ta'bga ko‘ra
Kinza – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Xamirni tayyorlash:
Shivitni suv bilan blenderda maydalang yoki mayda to‘g‘rab, suv bilan aralashtiring.
Tuxum, tuz va shivit suvidan tayyorlangan aralashmani idishga soling.
Un qo‘shib, o‘rtacha qattiqlikdagi xamir qorib, paketga o‘rab, muzlatgichga 20-25 daqiqaga qo‘ying.

2. Lag‘monni tayyorlash:
Xamirni muzlatgichdan olib, 1-2 mm qalinlikda yoying.
Xamirni 15 sm kenglikdagi chiziqlarga kesib, qurishi uchun 10-15 daqiqa qoldiring.
Rulet shaklida o‘rab, kengligi 1 sm bo‘lgan lag‘monlarni kesing.

3. Vaju tayyorlash:
Qozonga yog‘ solib, qizdiring va piyozni yumshaguncha qovuring.
Go‘sht qo‘shib, 3-4 daqiqa qovuring.
Pomidor pastasini qo‘shib, yana 3 daqiqa davomida qovuring.
Sabzi va kartoshkani qo‘shib, 3 daqiqa aralashtirib qovuring.
Bulg‘ori qalampiri, pomidor va sarimsoqni qo‘shib, aralashtiring.
Ziravorlarni solib, taxminan 2 litr suv qo‘shing va past olovda pishguncha qaynatib pishiring.

4. Lag‘monni pishirish:
Lag‘monni sho‘r suvda 2 daqiqa davomida pishiring.
Suvini to‘kib tashlab, lag‘monga ozroq o‘simlik yog‘i qo‘shib aralashtiring.

5. Xizmat qilish:
Lag‘monni likopchalarga solib, ustidan vaju quyib, ko‘katlar bilan bezang.
Tayyor shivit oshini issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_nonpalov": """Non palov🍞🍲
Masalliqlar: 🍱

O‘simlik yog‘i – ta'bga ko‘ra
Piyoz – 1 dona
Go‘sht – 200 g
Pomidor – 2 dona
Kartoshka – 2 dona
Bulg‘ori qalampiri – 1 dona
Sarimsoq – 2 bo‘lak
Qotgan non bo‘laklari – ta'bga ko‘ra
Ta'bga ko‘ra tuz va ziravorlar

Tayyorlash bosqichlari: 🍱

Masalliqlarni tayyorlash:
Barcha masalliqlarni archib, o‘zingizga yoqqan shaklda to‘g‘rang (somoncha shakl tavsiya etiladi).

Go‘shtni qovurish:
Qozonga o‘simlik yog‘i solib, qizdiring.
Mayda to‘g‘ralgan sarimsoqni qo‘shib, go‘shtni qovuring. Sarimsoq go‘shtga o‘zgacha ta'm beradi.

Piyoz va sabzavotlarni qo‘shish:
Piyozni qo‘shib, tillarang tusga kirguncha qovuring.
So‘ng bulg‘ori qalampirini qo‘shib, 2-3 daqiqa davomida qovuring.
Pomidorni qo‘shib, aralashtiring va biroz qovuring.
So‘ng kartoshkani qo‘shib, aralashtiring.

Nonni qo‘shish:
Tuz va ziravorlarni solib aralashtiring.
To‘g‘ralgan non bo‘laklarini qo‘shing va yaxshilab qovuring.

Dimlash:
Qozonga ozroq suv quying va qopqog‘ini yoping.
Olovni pastlatib, 5-10 daqiqa davomida dimlang. Nonlar juda ezilib ketmasligi uchun ehtiyot bo‘ling.

Maslahatlar:
Nonni o‘rtacha qalinlikda to‘g‘rang, juda qalin bo‘lsa qotib qolishi, juda yupqa bo‘lsa ezilib ketishi mumkin.
Quruq nonlar uchun o‘simlik yog‘ini ko‘proq qo‘shing yoki nonlarni oldindan sovuq suvda bir chayib oling.

Xizmat qilish:
Tayyor taomni ta'bga ko‘ra bezatib, issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_kartoshkadolma": """Kartoshka do'lma🧆
Masalliqlar: 🍱

Kartoshka – 10-15 dona
Go‘shtning yog‘li qismi yoki qiyma – 300-400 g
Piyoz – 300-400 g
Qaynatilgan guruch (yarim pishgan) – 100-200 g
O‘simlik yog‘i – ta'bga ko‘ra
Ta'bga ko‘ra tuz, ziravor va oshko‘kat

Tayyorlash bosqichlari: 🍱

1. Qiymaning tayyorlanishi:
Go‘sht va piyozni mayda kubik shaklida to‘g‘rang.
Guruch, oshko‘kat, tuz va ziravorlarni qo‘shib yaxshilab aralashtiring.
Agar go‘sht yoki qiyma yog‘siz bo‘lsa, charvi yog‘i yoki ozroq o‘simlik yog‘i qo‘shing.

2. Kartoshkani tayyorlash:
Kartoshkalarning ichini o‘yib, o‘ralar tayyorlang.
Ichidan kesib olingan kartoshka qoldiqlarini tashlamang – ularni boshqa taomlar uchun ishlatishingiz mumkin.

3. Kartoshkani qovurish:
Kartoshkalarni ichki qismini qizib turgan yog‘da biroz qizartirib qovuring.

4. Do‘lmani to‘ldirish:
Har bir kartoshkaning ichiga taxminan 70-80 g tayyor qiyma soling.

5. Pishirish:
Do‘lmalarni patnisga tering va oldindan qizdirilgan 180°C dimxonada 20-30 daqiqa davomida pishiring.
Istasangiz, oxirgi 5 daqiqada har bir do‘lmaning ustiga qirg‘ichdan o‘tkazilgan pishloq qo‘yib, yana pishirib oling.

6. Xizmat qilish:
Tayyor bo‘lgan do‘lmalarni lagan yoki taqsimchaga soling. Ta'bga ko‘ra ko‘katlar bilan bezab dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_dumbulpalov": """ Dumbul palov 🌽 🍲
Masalliqlar: 🍱

Yog‘ – 100 g
Go‘sht – 200 g
Piyoz – 4 dona
Sabzi – 3 dona
Kartoshka – 2 dona
Jo‘xori donalari – 5-6 dona jo‘xori
Pomidor – 3 dona
Sarimsoq – 5-6 bo‘lak
Bulg‘ori qalampiri – 2 dona
Tuz, ziravor va ko‘katlar – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

Masalliqlarni tayyorlash: 🍱
Sabzavotlarni kubik shaklda to‘g‘rang.
Piyozni xalqa shaklida, sarimsoqni mayda qilib to‘g‘rang.

Go‘shtni qovurish:
Qizigan yog‘da go‘shtni qovuring.
Go‘sht qovurilayotganda mayda to‘g‘ralgan sarimsoqni qo‘shib, aralashtiring.

Sabzavotlarni qo‘shish:
Go‘shtning ustiga xalqa shaklidagi piyozni qo‘shib, tillarang tusga kirguncha qovuring.
Sabzi va kartoshkani qo‘shib, aralashtirib qovuring.
Keyin pomidorni solib, yana aralashtirib pishiring.

Jo‘xori va bulg‘ori qalampiri:
Jo‘xori donalarini qo‘shib, aralashtirib biroz qovuring.
Bulg‘ori qalampirini qo‘shib, pishirishni davom ettiring.

Suv va ziravorlarni qo‘shish:
Qozonga kerakli miqdorda suv quyib, tuz va ziravorlarni seping.
To‘g‘ralgan ko‘katlarni taomning ustiga joylashtiring.

Dimlash:
Qozonning qopqog‘ini yopib, taomni 35-40 daqiqa davomida past olovda dimlab pishiring.

Xizmat qilish:
Tayyor bo‘lgan dumbul palovni ta'bga ko‘ra bezatib, issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_teftel": """Teftel 🧆 
Masalliqlar: 🍱

Sabzi (qizil) – 1 dona
Piyoz – 2 dona
Un – ta'bga ko‘ra
Guruch – 200 g
Tuxum – 1 dona
Tuz – ta'bga ko‘ra
Ukrop (ko‘kat) – ta'bga ko‘ra
Tomat pastasi – 1 osh qoshiq
Sarimsoq – 2 dona
Mol go‘shti qiymasi – 300 g
Murch – bir chimdim
Yog‘ – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

Qiymani tayyorlash:
Qiymaga guruch, mayda to‘g‘ralgan piyoz, sarimsoq, tuxum, tuz va ziravorlarni qo‘shib, yaxshilab aralashtiring.

Teftel shakllantirish:
Tayyor qiymadan yong‘oqdek kichik koptokchalar yasang.
Koptoklarni unga botirib oling.

Teftellarni qovurish:
Tovaga yog‘ solib, teftellarni oltin tusga kirguncha qovuring va chetga olib qo‘ying.

Qayla tayyorlash:
Qozonga yog‘ solib, piyozni qizartirib qovuring.
Qirg‘ichdan chiqarilgan sabzini qo‘shib, qovurishda davom eting.
Tomat pastasini qo‘shib, 1-2 marta aralashtiring.
1,5 litr suv qo‘shib, qaynatib chiqing.

Ziravorlar qo‘shish:
Qaylayga tuz, murch va mayda to‘g‘ralgan ko‘katlarni qo‘shing.

Teftellarni qaylaga solish:
Qovurilgan teftellarni qaylaga soling.
Teftellar qayla bilan to‘liq ko‘milgan bo‘lishi kerak.

Pishirish:
Qozon qopqog‘ini yopib, past olovda 30 daqiqa davomida dimlab pishiring.

Xizmat qilish:
Tayyor teftellarni guruch bilan yoki boshqa garnir bilan dasturxonga torting.
Yoqimli ishtaha! 🍽 😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_sarimsoqli": """
Sarimsoqpiyoz bilan pishirilgan kartoshka 🧆

Masalliqlar: 🍱
Kartoshka – 1 kg
Sarimsoqpiyoz – 8 tish
Zaytun moyi – 70 ml
Tuz va murch – ta'bga ko‘ra
Maydalangan petrushka – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Kartoshkani tayyorlash:
Kartoshkani po‘stini artmasdan yaxshilab yuvib tozalang.
Har bir kartoshkani 4 bo‘lakka bo‘ling va katta idishga joylashtiring.

2. Ziravorlar bilan aralashtirish:
Idishga zaytun moyi, tuz, murch va maydalangan sarimsoqpiyoz qo‘shing.
Kartoshkalarni yaxshilab aralashtirib, ziravorlar bilan to‘liq qoplanishini ta'minlang.

3. Pishirish uchun tayyorlash:
Kartoshkalarni toblatma idishiga bir qavat qilib terib chiqing.

4. Pishirish:
Gaz pechini 200°C darajaga qizdirib, kartoshkani 45-60 daqiqa davomida pishiring.
Kartoshkaning usti qarsildoq, ichi yumshoq bo‘lishi lozim.

5. Xizmat qilish:
Pishgan kartoshkani gaz pechidan olib, ustiga maydalangan petrushka sepib bezang.
Taomni issiq holda, garnir yoki asosiy yegulik sifatida dasturxonga torting.
Yoqimli ishtaha! 🍽 😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_begodi": """Begodi 🍛 
Masalliqlar: 🍱

Mol go‘shti – 300 g
Kartoshka – 1 dona
Piyoz – 1 dona
Un – 500 g
Suv – 1 stakan
Tuz – 1 osh qoshiq
Karam – 1 dona

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Kichkina karamni mayda qilib to‘g‘rang.
Piyozni ham mayda shaklda to‘g‘rang.
Mol go‘shtni mayda kubik shaklida yoki qiymalagichdan o‘tkazib tayyorlang.
Ixtiyoriy ravishda, kartoshkani mayda qilib to‘g‘rab qo‘shishingiz mumkin.

2. Xamirni tayyorlash:
Un, suv va tuzni aralashtirib xamir qorib oling.
Xamirni dumaloq shaklga keltirib, ustini paket yoki sochiq bilan yopib, 10 daqiqaga tindiring.

3. Begodini shakllantirish:
Tingan xamirdan kichik bo‘laklar olib, qo‘lda yoying.
Tayyorlangan masalliqlardan (go‘sht, karam, piyoz va kartoshka aralashmasi) bir qismini yoyilgan xamirning o‘rtasiga joylashtiring.
Xamir chetlarini rasmda ko‘rsatilganidek, yopib, begodi shaklida tugib chiqing.

4. Pishirish:
Tayyor begodilarni yog‘langan patnisga joylashtiring yoki bug‘da pishirish uchun mos qozonda bug‘da pishiring.
Dimlash uchun 20-25 daqiqa davomida past olovda pishiring.

5. Xizmat qilish:
Tayyor begodilarni issiq holda, ustiga ko‘katlar bilan bezab dasturxonga torting.
Yoqimli ishtaha! 🍽 😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_baliqlikotlet": """Baliqli katlet 🐟 🧆
Masalliqlar: 🍱

Baliq (qiltanoqdan tozalangan) – 500 g
Piyoz – 1 dona
Sarimsoq – 2 dona
Un – 3-4 osh qoshiq
Tuxum – 1 dona
Tuz – bir chimdim
Murch – bir chimdim
Yog‘ – qovurish uchun

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni maydalash:
Baliq, piyoz va sarimsoqni go‘sht qiymalagichdan o‘tkazing yoki blender yordamida maydalang.

2. Aralashmani tayyorlash:
Qiymaga tuxum, tuz, murch va un qo‘shib yaxshilab aralashtiring.

3. Kotletlarni shakllantirish:
Qo‘lingizni yog‘lab, qiymadan dumaloq yoki yassiroq shakldagi kotletlar yasang.

4. Qovurish:
Tovaga ozroq yog‘ solib, qizdiring.
Kotletlarni solib, har bir tomonini taxminan 3 daqiqa davomida oltin tusga kirguncha qovuring.

5. Xizmat qilish:
Tayyor baliqli kotletlarni issiq holda, garnir yoki salat bilan dasturxonga torting.
Yoqimli ishtaha! 🍽 😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_jigarkabob": """Jigar kabob 🥩 
Masalliqlar: 🍱

Jigar – 600 g
Dumba yog‘i – 200 g
Tuz va ziravorlar (qizil qalampir, qora murch, kashnich urug‘i, zira)

Tayyorlash bosqichlari: 🍱

Jigarni tayyorlash:
Jigarni pardasi va qotib qolgan qonlardan tozalang.
Uni 15 grammlik (3x3 sm) to‘rtburchak bo‘laklarga to‘g‘rang.

Dumba yog‘ini tayyorlash:
Dumbani jigarga nisbatan biroz uzunroq qilib to‘g‘rang.
Uzunroq to‘g‘ralgan dumba kabob pishish jarayonida sixda uzoqroq saqlanadi.

Ziravorlarni tayyorlash:
Yanchilgan qora murch, qizil qalampir, kashnich urug‘i, zira va tuzni aralashtirib ziravor qorishmasini tayyorlang.

Kabobni sixlash:
Jigar va yog‘ni navbatma-navbat sixga tizib chiqing.
Masalan, bir jigar, bir yog‘ yoki 4 ta jigar, 2 ta yog‘ tarzida joylashtiring.

Kabobni ziravorlash:
Pishirishdan oldin kabobning ustiga tayyorlangan ziravorni sepib chiqing.

Pishirish:
Kabobni qizib turgan cho‘g‘da, har tomoni qizarguncha pishiring.
Pishirish jarayonida kabobni muntazam ravishda aylantirib, bir xilda qizarib pishishini ta'minlang.

Xizmat qilish:
Tayyor kabobni yupqa qilib to‘g‘ralgan piyoz yoki garnir bilan birga dasturxonga torting.
Yoqimli ishtaha! 🍽 😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qozonkabob": """Qozon kabob 🫕🥩
Masalliqlar: 🍱

Mol go‘shti – 1 kg
Qo‘y yog‘i – 100 g
Kartoshka – 2 kg
Piyoz – 2 dona
Pomidor – 3 dona
O‘simlik moyi – 100 ml
Ziravorlar aralashmasi (yanchilgan zira, kashnich urug‘lari, quritilgan rayhon, qizil achchiq qalampir) – 3 osh qoshiq
Tuz – ta'bga ko‘ra
Shivit va kashnich – 5-7 shoxcha

Tayyorlash bosqichlari: 🍱

Go‘shtni tayyorlash:
Go‘shtni katta bo‘laklarga kesing.
2 osh qoshiq ziravor aralashmasi qo‘shib, aralashtiring.

Piyozni yarim halqa shaklida, pomidorni ingichka doira shaklida to‘g‘rang.
Piyoz, pomidor va ziravorlangan go‘shtni aralashtirib, sovutgichda 5-6 soat dam oldiring. Xohlasangiz, limon bo‘laklarini ham qo‘shishingiz mumkin.

Kartoshkani tayyorlash:
Kartoshkani tozalang va katta bo‘laklarga kesing (katta kartoshkalarni ikkiga bo‘ling).
Qo‘y yog‘ini mayda kubiklarga bo‘lib, qozonda eritib, jizzasini ajrating.
Kartoshkani eritilgan yog‘da tillarang tusga kirguncha qovuring va boshqa idishga chiqarib oling.

Go‘shtni qovurish:
Qozonga kartoshkadan oqib chiqqan yog‘ni qaytarib soling.
Go‘shtni qozonga solib, baland olovda jigarrang tusga kirguncha qovuring.
Go‘sht suvini chiqarib, bug‘lanishini kuting, so‘ng qovurishni davom ettiring.

Dimlash:
Go‘sht qovurilib jigarrang tusga kirgach, qozonga oz miqdorda suv quying (go‘shtni to‘liq qoplamasligi kerak).
Qopqoqni yopib, past olovda 20 daqiqa davomida dimlang.

Kartoshkani qo‘shish:
Qopqoqni ochib, qolgan suvni bug‘lantiring.
Kartoshkani qozonga qaytarib soling, tuz va qolgan ziravorlarni qo‘shib aralashtiring.
Yopiq qopqoq ostida yana 10 daqiqa davomida dimlang.

Xizmat qilish:
Tayyor qozon kabobini shivit va kashnich sepib, keng idishda dasturxonga torting.
Yoqimli ishtaha! 🍽 😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qiymalikabob": """Qiymali kabob 🥩🧆
Masalliqlar: 🍱

Go‘sht – 0,5 kg
Charvi yog‘i – 200 g
Piyoz – 100-150 g
Non bo‘laklari – bir necha dona
Tuz va ziravorlar – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

Qiymani tayyorlash:
Go‘sht, charvi yog‘i, piyoz va non bo‘laklarini qiymalagichdan o‘tkazing.
Agar qiymalagich teshiklari katta bo‘lsa, ikki marta; kichik bo‘lsa, bir marta o‘tkazish kifoya.
Qiymaga tuz va ziravorlarni qo‘shib, yaxshilab aralashtiring.

Qiymaning muzlatilishi:
Tayyorlangan qiymani tatib ko‘rib, kam-ko‘stini to‘g‘irlang.
Qiymaning yaxshiroq yopishishi va oqib ketmasligi uchun uni yarim soat yoki bir soatga muzlatgichga qo‘ying.

Kabobni shakllantirish:
Six uzunligiga qarab, qiymani 80-120 grammli bo‘laklarga bo‘ling.
Qo‘lingizni namlab, qiymadan bo‘laklar olib, sixlarga yaxshilab o‘rang.

Kabobni muzlatish:
Agar olov hali tayyor bo‘lmasa, sixlangan kaboblarni yana muzlatgichga qo‘yib qo‘ying. Bu qiyma qizib, bir-biriga yopishib qolmasligi uchun muhimdir.

Pishirish:
Kaboblarni ko‘mir ustiga qo‘yib, har ikki tomoni oltin tusga kirguncha qovuring.
Cho‘g‘ ustiga qo‘yilganda usti biroz kul bilan qoplangan bo‘lishi kerak.
Kabobning hajmiga qarab, uni 5-8 daqiqa davomida pishiring.

Xizmat qilish:
Tayyor kaboblarni ta'bga ko‘ra bezang.
Sous yoki salat bilan birga dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_tandirkabob": """Tandir kabob 🧆
Masalliqlar: 🍱

Tovuq – 1 dona
Apelsin – 1 dona
Qaymoq – 1-2 osh qoshiq
Sarimsoq – 5-6 bo‘lak
Archa shoxchalari (yoki rozmarin, timyan)
Ta'bga ko‘ra tuz va ziravorlar

Tayyorlash bosqichlari: 🍱

1. Marinad tayyorlash:
Apelsin suvini siqib oling.
Qaymoq, mayda chopilgan sarimsoq, tuz va ziravorlarni apelsin suvi bilan aralashtirib, bir hil massa tayyorlang.

2. Tovuqni marinadlash:
Tayyorlangan massani tovuqning ichi va ustiga yaxshilab surtib chiqing.
Tovuqni archa shoxchalari yoki boshqa o‘simliklar bilan o‘rab, bir necha soat davomida tindirib qo‘ying.
(Maslahat: Tovuqni marinadlangan suyuqlikda to‘liq botirib qo‘yib, yanada mazali qilish uchun bir necha soat saqlashingiz mumkin.)

3. Tovuqni tandirga joylash:
Marinadlangan tovuqni temirga ilib, tandirga joylang.
Tandir ichiga ozroq suv solingan temir idishni qo‘ying. Bu tandirning ichidagi namlikni saqlash va kabobning qurib qolmasligini ta'minlash uchun kerak.
Ilingan tovuq ostiga to‘g‘ralgan sabzavotlarni (masalan, kartoshka, sabzi, piyoz) joylashtiring. Bu sabzavotlar pishganida kabobga mazali garnir bo‘lib xizmat qiladi.

4. Tandirni yopish:
Tandir harorati taxminan 150-160°C bo‘lishi kerak.
Tandirning ustini havo kirmaydigan qilib qopqoq yoki folga bilan yopib qo‘ying.

5. Kabobni pishirish:
Tandir kabobni taxminan 2 soat davomida dimlang.
Go‘sht yaxshi pishishi uchun haroratni doimiy saqlang.

6. Xizmat qilish:
Tayyor bo‘lgan tandir kabobni avval sabzavotlarni olib, so‘ngra kabobni ustiga joylashtiring.
Ta'bga ko‘ra bezatib, issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_tovuqkabob": """Tovuq kabob 🍗🧆
Masalliqlar: 🍱

Tovuq go‘shti – 1 kg
Mayonez – 2-3 osh qoshiq
Sarimsoq – 4-5 bo‘lak
Qizilcha (quritilgan pomidor yoki bulg‘ori maydasi) – ta'bga ko‘ra
Tuz va ziravorlar – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Tovuqni tayyorlash:
Tovuq go‘shtini juda ham katta va juda ham kichik bo‘lmagan (20-30 g) bo‘laklarga bo‘ling.
Tayyor bo‘laklarni idishga soling.

2. Marinad tayyorlash:
Tovuq bo‘laklariga mayonez, tuz, ziravorlar va mayda to‘g‘ralgan sarimsoqni qo‘shing.
Hammasini yaxshilab aralashtiring.
Agar vaqtingiz bo‘lsa, tovuqni bir necha soat muzlatgichda tindirib qo‘ying.

3. Sixlash:
Marinadlangan go‘shtni sixlarga tizing. Har bir sixga 4-6 dona go‘sht bo‘lagi sig‘ishi mumkin.
Sixlangan kaboblarning ustiga qizilcha seping.

4. Kabobni pishirish:
Kaboblarni qizib turgan cho‘g‘ ustida pishiring.
Har tomonini doimiy aylantirib, go‘shtni teng qizartiring.

5. Xizmat qilish:
Tayyor kaboblarni didingizga ko‘ra bezab, issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_namangankabob": """Namangan kabob 🧆
Masalliqlar: 🍱

Qo‘y go‘shti (yumshoq qismi) – 1 kg
Piyoz – 2-3 dona
Dumba yog‘i – 200-300 g
Tuz va ziravorlar – ta'bga ko‘ra
Talqon yoki un – ta'bga ko‘ra
Gazli suv – 250 ml

Tayyorlash bosqichlari: 🍱

1. Go‘shtni tayyorlash:
Go‘shtni yumshoq qismini paylardan tozalang.
15-20 grammli bo‘lakchalarga kesing.
Bo‘laklarni urib latlang, bu go‘shtni yumshoq qiladi.

2. Marinad tayyorlash:
Piyozni yarim halqa shaklida to‘g‘rang.
Gazli suv, tuz va ziravorlarni qo‘shib, go‘sht bilan aralashtiring.
Go‘shtni kamida 5-6 soat davomida marinadlash uchun qoldiring.

3. Dumbani tayyorlash:
Dumbani go‘shtga nisbatan maydaroq bo‘laklarga kesing.
Marinadlangan go‘sht va dumbani navbatma-navbat sixga tizing.

4. Kabobni tayyorlash:
Sixlangan kabob ustiga un yoki talqon va yanchilgan qizil bulg‘or qalampirini seping.
Tandirda 15-20 daqiqa davomida pishiring.

5. Zamonaviy usul (ixtiyoriy):
Kabobni tandirga qo‘yishdan oldin ustiga somsa xamirini o‘rang.
Xamir ustiga qatiq yoki sut kukunini suv bilan aralashtirib surtib, kunjut yoki sedana seping.
Tandirda 20-25 daqiqa davomida qizartirib pishiring.

6. Tandirda pishirish:
Sixlarni tandir ichiga joylashtirish uchun g‘isht yoki tog‘orachadan foydalaning yoki ilmoqlarga iling.
Tandir harorati doimiy bo‘lishi kerak.

7. Xizmat qilish:
Tayyor kabobni ta'bga ko‘ra bezab, issiq holda dasturxonga torting.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_norin": """Norin🍝 
     Masalliqlar: 🍱
• Un – 400 g
• Tuxum – 1 ta
• Tuz – 15 g
• Suv – 150 ml
• Ot go‘shti – 700 g
• Qazi – 1 ta
• O‘simlik yog‘i

Tayyorlash usuli: 🍱
Qadam 1:
Un, tuxum, suv va tuzni aralashtirib, qattiq xamir qoriladi. Xamirni 20 daqiqa tindirib qo‘yiladi.

Qadam 2:
Tindirilgan xamirni juda yupqa qilib yoyiladi va taxminan 20x20 sm hajmda kvadrat shaklida kesiladi.

Qadam 3:
Katta qozonga suv solib, ozgina tuz qo‘shiladi va qaynashga qo‘yiladi. Xamir bo‘laklari qaynoq suvga 2-3 tadan solinib, bir marta qaynab chiqquncha pishiriladi.

Qadam 4:
Pishgan xamirlarni suzg‘ich yordamida suvdan olib, yopishmasligi uchun o‘simlik yog‘i surtiladi. So‘ngra xamirlarni tekis qilib yoyib quritiladi. Har ikki tomoni quriganidan keyin yog‘lab, taxlanadi.

Qadam 5:
Yog‘langan xamirlarni 4-5 sm kenglikdagi lentaga bo‘lib, lentalarni ustma-ust joylab, mayda qilib ugra shaklida to‘g‘raladi.

Qadam 6:
Ot go‘shti va qazi tuzli suvda miltillatib qaynatiladi (taxminan 1-1,5 soat). Qaynatilgan go‘sht mayda qilib to‘g‘raladi.

Qadam 7:
Ug‘ralangan xamir, to‘g‘ralgan go‘sht va o‘simlik yog‘i birlashtirilib aralashtiriladi. Ta’bga ko‘ra, ziravorlar va maydalangan zira qo‘shiladi.

Qadam 8:
Norinni likopchalarga solib, ustiga qazi bo‘laklari va mayda to‘g‘ralgan piyoz bilan bezatib tortiladi.

Maslahatlar:
• Xamirlarni juda yupqa yoyish norinning chiroyli va mazali bo‘lishi uchun muhim.
• Xamirni yog‘lash va quritish jarayonlariga alohida e’tibor bering, shunda xamirlar yopishib qolmaydi.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_xasip": """Xasip 🥓
    Masalliqlar: 🍱
• Qo‘y ichagi – 1 ta
• Qo‘y go‘shti – 200 g
• Qora taloq (qo‘yniki) – 1 ta
• Qo‘y buyragi – 1 ta
• Qo‘y o‘pkasi – 200 g
• Qo‘y dumbasi – 100 g
• Guruch – 200 g
• Piyoz – 4-5 dona
• Tuz, qora murch, zira, kashnich urug‘i – ta'bga ko‘ra

Tayyorlash usuli: 🍱
1. Masalliqlarni tayyorlash:
Go‘sht, dumba va ichki a'zolarni (o‘pka, buyrak, qora taloq) qiymalagichdan o‘tkazing.
Guruchni oldindan yuvib, quritib oling.

2. Aralashmani tayyorlash:
Qiymaga mayda chopilgan piyoz, guruch, tuz, qora murch, zira va maydalangan kashnich urug‘ini qo‘shib yaxshilab aralashtiring. Suvliroq qiymani tayyorlash uchun ozgina iliq suv qo‘shing. Bu ichakka oson quyilishini ta’minlaydi.

3. Ichakni to‘ldirish:
Yuvilgan va tozalangan qo‘y ichagini voronka yordamida tayyorlangan qiymaga to‘ldiring.
Ichakni haddan ortiq to‘ldirmang, aks holda qaynash vaqtida yorilib ketishi mumkin.
Ichakning ikkala uchini ip yordamida mahkam bog‘lang.

4. Pishirish:
Katta qozonga suv solib, ichaklarni ehtiyotkorlik bilan soling. Suv qaynashini past darajaga tushirib, taxminan 40 daqiqa davomida miltillatib qaynatib pishiring. Juda baland olovda qaynatishdan saqlaning, chunki bu xasipning yorilishiga olib kelishi mumkin.

5. Taqdim etish:
Pishgan xasipni laganga yoki likopchaga joylashtirib, ta'bingizga ko‘ra bezating. Uni yangi sabzavotlar, ko‘katlar yoki bodring bilan birga tortiq qilish mumkin.
Maslahatlar:
• Ichakni yaxshilab tozalash va tuzli suvda chayib yuvish kerak.
• Ziravorlarni o‘z didingizga qarab ko‘paytirishingiz yoki kamaytirishingiz mumkin.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_tuxumbarak": """Tuxum barak 🥟
    Masalliqlar: 🍱
Xamir uchun:
• Un – 200 g
• Tuxum oqi – 1 dona
• Suv – 100 ml
• Tuz – ta'bga ko'ra

Ichiga:
• Tuxum – 4-5 dona
• Sut – 100 ml
• O‘simlik yog‘i – 2-3 osh qoshiq
• Tuz – ta'bga ko'ra
• Ko‘kat va ziravorlar – ta'bga ko'ra

Tayyorlash usuli: 🍱
1. Xamirni tayyorlash:
Un, tuxum oqi, suv va tuzni aralashtirib, o‘rta qattiqlikdagi xamir qoriladi. Tayyor xamirni 15-20 daqiqaga tindirib qo‘yiladi.

2. Ichki masalliqlarni tayyorlash:
Tuxumlarni idishga chaqib, yaxshilab iylab aralashtiring. Ustiga sut, o‘simlik yog‘i, tuz va ziravorlar qo‘shib, bir hil holatga kelguncha aralashtiring. Agar xohlasangiz, mayda to‘g‘ralgan ko‘katlarni ham qo‘shing.

3. Xamirni yoyish va jild tayyorlash:
Xamirni 5-6 grammlik zuvalachalarga bo‘lib, juva yordamida yupqa qilib yoying. Yoyilgan xamirni ustma-ust qilib taxlab, orasiga ozgina un seping. Har bir xamir bo‘lagini yarim buklab, chetlarini mahkam bosib chiqib, jild tayyorlang.

4. Qaynatishga tayyorlash:
Qaynoq suv solingan idishni tayyorlang va suvga ozroq tuz soling.

5. Baraklarni ichini to‘ldirish:
Jildning ochiq qismidan ichiga 1-2 qoshiq tuxumli aralashmani quying. Shoshilmasdan ochiq qismini yopib, chetlarini mahkam yopishtiring.

6. Pishirish:
Tayyorlangan baraklarni qaynab turgan suvga birin-ketin soling. Baraklar suv yuziga ko‘tarilsa, ular pishgan hisoblanadi.

7. Sovutish va yog‘lash:
Tayyor tuxumbaraklarni chovli yordamida olib, sovuq suvda chayib oling va yopishib qolmasligi uchun biroz yog‘ surting.

8. Taqdim etish:
Tuxum baraklarni qatiq, suzma yoki qaymoq bilan bezatib, dasturxonga tortiq qiling.

Maslahatlar:
• Xamirni juda yupqa qilib yoyish tuxum barakni yumshoqroq qiladi.
• Tuxumli ichini choynak yordamida quysangiz, osonroq bo‘ladi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

})  # <-- .update() ni yakunlash
# ---- KODNING DAVOMI (4-QISM, C) ----

recipes_texts.update({

    # ---------- SALATLAR BO‘LIMI ----------
    "dish_achchiqchuchuk": """Achchiq chuchuk salat🥗 
    Masalliqlar: 🍱

Pomidor – 500 g
Piyoz – 2 dona (qizil piyoz tavsiya etiladi)
Rayhon – ta'bga ko‘ra
Tuz – ta'bga ko‘ra
Qora murch – ta'bga ko‘ra
Achchiq qalampir – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni to‘g‘rash:
Pomidorni o‘tkir pichoq yordamida qo‘lda yoki oshtaxtada yupqa yarim halqa shaklida to‘g‘rang.
Piyozni ham xuddi shunday shaklda to‘g‘rang. Agar piyozning achchig‘i kuchli bo‘lsa, uni sovuq suvda chayib oling.

2. Rayhonni qo‘shish:
Tug‘ralgan rayhonni pomidor va piyozga qo‘shing.

3. Ziravorlash:
Tuz, qora murch va ta'bga ko‘ra achchiq qalampir qo‘shib, yaxshilab aralashtiring.

4. Xizmatga tayyorlash:
Salatni likopcha yoki salat uchun mo‘ljallangan idishga joylashtiring.
Agar salatga chiroyli shakl berishni istasangiz, maxsus qoliplardan foydalanishingiz mumkin.

Maslahat:
Ushbu salatni quyuq taomlar bilan yoki alohida yegulik sifatida dasturxonga tortishingiz mumkin.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_bodringbrinza": """Bodring va brinzali salat 🥒🥗
    Masalliqlar: 🍱

Bodring – 250 g
Brinza – 150 g
Salat barglari – 1 bog‘
O‘simlik yog‘i – 2 osh qoshiq
Limon sharbati – yarim limon
Tuz va murch – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Bodring va salat barglarini yaxshilab yuvib, quriting.
Brinza va bodringni to‘rtburchak shaklda, salat barglarini yirik qilib to‘g‘rang.

2. Aralashtirish:
Tayyorlangan masalliqlarni bir idishga solib, yaxshilab aralashtiring.

3. Ziravorlash:
Salatga o‘simlik yog‘ini qo‘shib, yana aralashtiring.
Limon sharbatini sepib, ta'bga ko‘ra tuz va murch qo‘shing.

4. Xizmat qilish:
Tayyor salatni likopchaga joylashtiring va dasturxonga torting.

Maslahat:
Ushbu salat vitaminlarga boy bo‘lib, kam kaloriyali taomlar uchun juda mos keladi. Yengil tushlik yoki asosiy taom oldidan gazak sifatida tortilishi mumkin.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_karampomidor": """Karam va pomidorli salat 🥬🥗
    Masalliqlar: 🍱

Karam – 500 g
Bodring – 200 g
Pomidor – 300 g
Shivit – yarim bog‘
Shakar – 1 choy qoshiq
Sarimsoq – 1 dona tishcha
Olma sirkasi – 2 choy qoshiq
Zaytun moyi – 2 osh qoshiq
Tuz va murch – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Karamni tayyorlash:
Karamni yupqa somoncha shaklida to‘g‘rang.
Ustidan shakar va ozgina tuz sepib, qo‘llaringiz bilan yaxshilab ishqalang. Bu karamni yumshoq va mazali qiladi.

2. Sabzavotlarni to‘g‘rash:
Pomidor va bodringni qayroqcha shaklida to‘g‘rang.
Shivitni mayda qilib to‘g‘rab qo‘ying.

3. Salatni aralashtirish:
Karam ustiga pomidor, bodring, shivit va mayda to‘g‘ralgan sarimsoqni qo‘shing.
Ta'bga ko‘ra tuz va murch sepib, olma sirkasi hamda zaytun moyini qo‘shing.
Yaxshilab aralashtiring.

4. Xizmat qilish:
Tayyor bo‘lgan salatni likopchaga joylashtiring va darhol dasturxonga torting.

Maslahat:
Ushbu salatni nafaqat tushlik yoki kechki ovqatda, balki asosiy taom oldidan gazak sifatida ham iste’mol qilishingiz mumkin.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_gruzincha": """Gruzincha salat🥗
    Masalliqlar: 🍱

Bodring – 2 dona
Shirin-nordon olma – 2 dona
Limon sharbati – 1 choy qoshiq
Shivit – bir-ikki shoxcha
Sarimsoq – 1 dona tishcha
Zaytun yoki o‘simlik yog‘i – 1 choy qoshiq
Tuz – ta'bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Bodring va olmalarni tayyorlash:
Bodring va olmani koreyscha sabzili salat uchun mo‘ljallangan qirg‘ichdan o‘tkazing yoki yupqa somoncha shaklida to‘g‘rang.
Barchasini tog‘orachaga soling.

2. Shivit va sarimsoqni tayyorlash:
Shivitni mayda to‘g‘rang.
Sarimsoqpiyozni maydalang yoki qirg‘ichdan o‘tkazing.

3. Salatni aralashtirish:
Bodring va olmalarga shivit va sarimsoqni qo‘shing.
Tuz, limon sharbati va zaytun yoki o‘simlik yog‘ini qo‘shib, yaxshilab aralashtiring.

4. Xizmat qilish:
Tayyor salatni likopchaga joylashtiring va dasturxonga torting.

Maslahat:
Bu salat sersuv va yengil bo‘lib, har qanday taom oldidan yoki gazak sifatida mazali va foydali bo‘ladi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qarsildoq": """Qarsildoq salat 🥗
    Masalliqlar: 🍱

Piyoz – 150 g
Bodring – 300 g
Kungaboqar yog‘i – 4 osh qoshiq
Sarimsoqpiyoz – 1 dona
Tuz – ta'bga ko‘ra
Tuyilgan qora murch – ta'bga ko‘ra
Sirka – 1 osh qoshiq
Pishloq – 150 g
Tovuq filesi – 250 g
Salat bargi – 1 bog‘
Oq baton – 200 g

Tayyorlash bosqichlari: 🍱

1. Tovuqni tayyorlash:
Tovuq go‘shti filesini taxminan 20 daqiqa davomida qaynatib pishiring va sovuting.
Sovugan filelarni tolalarga ajrating.

2. Batonni tayyorlash:
Oq batonni kubik shaklida to‘g‘rang va o‘simlik yog‘ida tilla rang tusga kirguncha qovuring.

3. Sabzavotlarni tayyorlash:
Bodringni uzunchoq shaklda to‘g‘rang.
Piyozni yarim halqa qilib to‘g‘rang.
(Agar piyoz achchiq bo‘lsa, uni qaynoq suvga 10 daqiqaga solib qo‘ying va sovuq suvda chayib tashlang.)

4. Pishloqni tayyorlash:
Pishloqni mayda qirg‘ichdan o‘tkazing.

5. Gazak tayyorlash:
4 osh qoshiq o‘simlik yog‘iga sirka, maydalangan sarimsoq, tuz va qora murchni qo‘shib yaxshilab aralashtiring.

6. Salatni yig‘ish:
Salat barglarini qo‘lda maydalab, idishga joylashtiring.
Ustiga bodring, piyoz, tovuq filesi, gazak, pishloq va qovurilgan non bo‘laklarini soling.

7. Xizmat qilish:
Qovurilgan non bo‘laklarini salatga dasturxonga tortishdan oldin qo‘shish tavsiya etiladi, bu ularning qarsildoqligini saqlab qoladi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_suzmali": """Suzmali salat🥗 
    Masalliqlar: 🍱

Bodring – 1 dona
Suv – 1 stakan
Tuz – bir chimdim
Tuyilgan qora murch – bir chimdim
Suzma – 500 g
Kashnich – 300 g
Ukrop – 300 g
Rayhon – 15 dona barg
Yalpiz – 15 dona barg
Rediska – 4 dona

Tayyorlash bosqichlari: 🍱

1. Suzmani tayyorlash:
Suzmaga ozroq suv qo‘shib, qatiq quyuqligiga kelguncha aralashtiring.

2. Ko‘katlar va sabzavotlarni tayyorlash:
Kashnich, ukrop, rayhon va yalpiz barglarini mayda qilib to‘g‘rang.
Bodringni somoncha shaklida to‘g‘rang.
Redislarni ingichka doira shaklida to‘g‘rang.

3. Barchasini aralashtirish:
Suzmaga mayda to‘g‘ralgan ko‘katlar, bodring va redislarni qo‘shing.
Tuz va murch sepib, yaxshilab aralashtiring.

4. Xizmat qilish:
Tayyor bo‘lgan salatni likopchaga solib, nonga surkab yeyish yoki alohida taom sifatida dasturxonga torting.

Maslahat:
Bu salatni bahor va yoz mavsumida tayyorlash juda foydali, chunki u vitaminlarga boy va yengil ovqat hisoblanadi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_penchuza": """Penchuza salat 🥗
    Masalliqlar: 🍱

Kraxmalli lapsha – 200-250 g
Bodring – 170 g
Har xil rangli bulg‘or qalampiri – 100 g
Sabzi – 200 g
Piyoz – 60 g
O‘simlik yog‘i – 100 ml
Kunjut – 2 choy qoshiq
Sarimsoq – 4 dona tishcha
Tuz – 1 choy qoshiq
Shakar – 1 choy qoshiq
Sirka (70%) – 1 osh qoshiq
Soya qaylasi – 3 choy qoshiq
Achchiq qizil qalampir kukuni – ta'bga ko‘ra
Maydalangan kashnich – ta'bga ko‘ra
Shivit yoki kashnich – 0,5 bog‘

Tayyorlash bosqichlari: 🍱

1. Lapshani tayyorlash:
Kraxmalli lapshani qaynagan suvda 5-7 daqiqa davomida pishirib, keyin sovuq suvda yuvib tozalang.

2. Sabzavotlarni tayyorlash:
Bodring, bulg‘or qalampiri, sabzi va piyozni mayda somoncha shaklida to‘g‘rang.
Sarimsoqni maydalang.

3. Sabzavotlarni qovurish:
Sabzavotlarni alohida-alohida, har birini 2-3 daqiqa davomida qarsildoqligini saqlab qolish uchun o‘simlik yog‘ida yengilgina qovuring.

4. Aralashtirish:
Tayyorlangan lapsha va qovurilgan sabzavotlarni aralashtiring.
Ustiga maydalangan sarimsoq, tuz, shakar, achchiq qalampir kukuni, sirka va soya qaylasini qo‘shing.
Maydalangan kashnich va shivit yoki kashnichni qo‘shib, yaxshilab aralashtiring.

5. Tindirish:
Salatni 30 daqiqa davomida tindirib qo‘ying, shunda barcha ta'mlar uyg‘unlashadi.

6. Xizmat qilish:
Tayyor salatni likopchaga joylashtirib, dasturxonga torting.

Maslahat:
Pentuza salati o‘zining qarsildoqligi va boy ta'mi bilan ajralib turadi. U har kuni uchun mazali va foydali variant bo‘lib xizmat qiladi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_mandarin": """Mandarin salat🍊🥗
    Masalliqlar (6 porsiya uchun): 🍱

Qaynatilgan sabzi – 4 dona
Qaynatilgan tuxum – 3 dona
Qattiq pishloq – 120 g
Qaynatilgan tovuq filesi – 150 g
Sarimsoqpiyoz – 1 dona tishcha
Mayonez – 30 ml
Tuz – 1 choy qoshiq
Qora murch – 1 choy qoshiq

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Tuxum, sabzi va tovuq filesini qaynatib, sovutib oling.

2. Qirg‘ish va to‘g‘rash:
Tuxum, pishloq va sarimsoqpiyozni mayda qirg‘ichdan o‘tkazing.
Tovuq filesini mayda kubik shaklida to‘g‘rang.

3. Barcha masalliqlarni aralashtirish:
Idishda tuxum, pishloq, sarimsoqpiyoz, tovuq filesi, mayonez, tuz va qora murchni aralashtirib, bir hil massa hosil qiling.

4. Mandarin shakli yasash:
Tayyorlangan aralashmadan dumaloq koptokchalar yasang.

5. Sabzini tayyorlash:
Sabzini mayda qirg‘ichdan o‘tkazing va sharbatini siqib oling.
Sabziga bir chimdim tuz va 1 osh qoshiq mayonez qo‘shib, aralashtiring.

6. Mandarin shaklini tugatish:
Plastmassa plyonka bo‘lagiga 1 osh qoshiq sabzini yoyib, o‘rtasiga tuxum va tovuqli koptokchani qo‘ying.
Plyonka yordamida salatni mandarin shakliga keltiring.

7. Xizmat qilish:
Tayyor «mandarinchalarni» likopchaga joylashtiring va ustini qora murch donalari va ismaloq barglari bilan bezating.

Maslahat:
Bu yorqin va ishtaha ochar salat yangi yil dasturxoningizni bezatib, mehmonlaringizni lol qoldiradi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_tovuqlisalat": """Tovuqli salat 🍗🥗
    Masalliqlar: 🍱

Sarimsoqpiyoz – ta'bga ko'ra
Tuz – ta'bga ko'ra
Tuyilgan qora murch – ta'bga ko'ra
Selderey – 3 shox
Tovuq filesi – 2 dona
Ko‘k piyoz – ta'bga ko'ra
Yong‘oq – 30 g
Zaytun yog‘i – 3 osh qoshiq
Sirka (musallaslik) – 1 osh qoshiq
Zaytun – 80 g

Tayyorlash bosqichlari: 🍱

1. Tovuq go‘shtini tayyorlash:
Tovuq filesini qaynatib, sovuting.
Uzunchoq shaklda to‘g‘rang.

2. Sabzavot va qo‘shimchalarni tayyorlash:
Piyoz, selderey, pomidor va zaytunni bo‘laklarga to‘g‘rang.
Yong‘oqni maydalang.

3. Sous tayyorlash:
Bir idishda sirka, zaytun yog‘i, tuz, qora murch va maydalangan sarimsoqpiyozni aralashtiring.

4. Salatni yig‘ish:
Tovuq, sabzavotlar va zaytunni bir idishga soling.
Ustidan sousni quyib, yaxshilab aralashtiring.

5. Xizmat qilish:
Tayyor salatni likopchaga joylashtiring va maydalangan yong‘oq bilan bezating.

Maslahat:
Ushbu sodda va mazali salat oson tayyorlanishi bilan dasturxoningizni boyitadi va oila a’zolaringizni xursand qiladi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_smak": """Smak salat 🥗
    Masalliqlar: 🍱

Qattiq pishloq – 70-80 g
Pomidor – 3-4 dona (o‘rtacha kattalikdagi)
Sarimsoq – 2 dona
Shivit – yarim shingil
Suxariklar – 100 g
Tuz va murch – ta’bga ko‘ra
Mayonez yoki smetana – to‘ldirish uchun

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Pishloqni suxariklar kabi kichik kubik shaklida kesing.
Pomidorlarni xuddi shunday shaklda to‘g‘rang.

2. Asosiy aralashma:
Bir idishga pishloq va pomidorni soling.
Mayda to‘g‘ralgan shivit va ezilgan sarimsoqni qo‘shing.

3. Ziravorlar va sous:
Ta’bga ko‘ra tuz va murch sepib, mayonez yoki smetana qo‘shing.
Barchasini yaxshilab aralashtiring.

4. Suxariklarni qo‘shish:
Dasturxonga tortishdan oldin suxariklarni salatga qo‘shib, aralashtiring. Bu ularning qarsildoqligini saqlab qoladi.

Maslahat:
Ushbu salatni zaytun moyi bilan ham to‘ldirish mumkin.
Suxariklarni o‘zingiz tayyorlasangiz, salatning ta’mi yanada mazali chiqadi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_ozdiruvchi": """Ozdiruvchi salat🥗 
    Masalliqlar: 🍱

Qizil lavlagi – 1 dona
Qizil sabzi – 2 dona
Karam – 300 g
Zaytun moyi – 2 osh qoshiq
Limon sharbati – 1 osh qoshiq
Tuz – yarim choy qoshiq

Tayyorlash bosqichlari: 🍱

1. Karamni tayyorlash:
Karamni mayda qilib somoncha shaklida to‘g‘rab oling.

2. Sabzi va lavlagini tayyorlash:
Sabzi va lavlagining po‘stini artib, katta tishchali qirg‘ichdan o‘tkazing.

3. Aralashtirish:
Tayyorlangan sabzavotlarni tog‘orachaga soling.
Ustiga limon sharbati va zaytun moyini quying.
Tuz seping va yaxshilab aralashtiring.

Maslahat:
Istasangiz, maydalangan ko‘katlar (shivit yoki kashnich) bilan bezashingiz mumkin.
Bu salat ovqatlanish oralig‘ida yoki asosiy taom oldidan iste’mol qilish uchun juda mos keladi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_mevali": """Mevali salat🍌🥗 
    Masalliqlar: 🍱

Banan – 1 dona
Olma – 1 dona
Kivi – 1 dona
Yogurt – 100 g

Tayyorlash bosqichlari: 🍱

1. Mevalarni tayyorlash:
Banan, olma va kivini yuvib, po‘stidan tozalang.
Har birini mayda kubik shaklida to‘g‘rang.

2. Salatni aralashtirish:
Tayyorlangan mevalarni bir idishga soling.
Ustiga yogurt qo‘shing va yaxshilab aralashtiring.

3. Xizmat qilish:
Salatni 1 soat muzlatgichda tindirib, sovuq holda dasturxonga torting.

Maslahat:
Sharbat qo‘shishni xohlasangiz, mango yoki apelsin sharbatidan foydalaning.
C vitaminiga boy sitrus mevalar (apelsin, mandarin) qo‘shib, salatni yanada foydali qiling.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_braslet": """Braslet salat 🥗
    Masalliqlar: 🍱

Kartoshka – 2 dona
Sabzi – 1 dona
Piyoz – 1 dona
Lavlagi – 1 dona
Mayonez – ta'bga ko'ra
Tovuq boldiri – 300 g
Anor – 1 dona

Tayyorlash bosqichlari: 🍱

1. Tayyorlash:
Kartoshka, sabzi, lavlagi va tovuq go‘shtini tuzli suvda qaynatib pishiring.
Tovaga ozgina yog‘ solib, piyoz va qaynagan tovuq go‘shtini birga qovuring.

2. Sabzavotlarni tayyorlash:
Qaynagan sabzavotlarni qirg‘ichdan chiqaring.

3. Salatni yig‘ish:
Lagan o‘rtasiga stakan qo‘yib, atrofini qatlamma-qatlam yig‘ing:
Kartoshka → mayonez surting
Sabzi → mayonez surting
Tovuq go‘shti → mayonez surting
Lavlagi → mayonez surting
Oxirida yuzasini anor donalari bilan bezang.

4. Tindirish:
Salatni muzlatgichda 2 soat tindiring.

5. Xizmat qilish:
Muzlatgichdan olib, lagan o‘rtasidagi stakanni ehtiyotkorlik bilan oling. Salat xizmatga tayyor!

Maslahat:
Salatni taqdim etishdan oldin qo‘shimcha ko‘katlar bilan bezashingiz mumkin.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qotgannonli": """Qotgan nonli salat 🥗
    Masalliqlar: 🍱

Pomidor – 2 dona
Bodring – 2 dona
Nami qochgan non – 200 g
Zaytun – 200 g
Salat bargi – 1 bog‘

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Pomidor, bodring, zaytun va salat barglarini to‘rtburchak shaklda to‘g‘rang.
Nami qochgan nonni kubik shaklida maydalang.

2. Aralashtirish:
Barcha to‘g‘ralgan masalliqlarni bir idishga soling.
Tuz va mayonez qo‘shib yaxshilab aralashtiring.

3. Nonni qo‘shish:
Salatni iste'mol qilishga yaqin qotgan non bo‘lakchalarini qo‘shib, aralashtiring.

Maslahat:
Qotgan nonni o‘simlik yog‘ida engil qovurib, salatga qo‘shsangiz, yanada mazali bo‘ladi.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_goshtlisa": """Go'shtli salat 🥩🥗
    Masalliqlar: 🍱

Qaynatilgan mol go‘shti – 120-140 g
Pomidor – 2-3 dona
Bodring – 1-2 dona
Olma (kichikroq) – 1 dona
Qizil bulg‘ori qalampiri – 1 dona
Zaytun – 5-6 dona
Ketchup – 2 osh qoshiq
Mayonez – 3 osh qoshiq
Ta'bga ko‘ra: kunjut, tuz, murch, shivit (ukrop) va achchiq sous (lozijon, sous chili yoki achiqa)

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Qaynatilgan go‘sht, bodring, olma va qizil bulg‘orini somoncha shaklida to‘g‘rang. Agar bulg‘ori katta bo‘lsa, yarimtasi yetarli bo‘ladi.

2. Sous tayyorlash:
Ketchup, mayonez va achchiq sousni aralashtirib, sous hosil qiling.

3. Salatni aralashtirish:
Tug‘ralgan mahsulotlarga tayyor sousni qo‘shing.
Ta'bga ko‘ra tuz, murch va shivit qo‘shib, yaxshilab aralashtiring.

4. Bezatish:
Pomidorni dumaloq, yupqa parraklarga kesib, likopcha atrofiga terib chiqing.
Tayyorlangan salatni likopning o‘rtasiga baland qilib joylashtiring.
Chekka qismlarini halqa shaklida kesilgan zaytun bilan bezang.
Ustidan kunjut sepib, dasturxonga tortiq qiling.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_karamli": """Karamli salat 🥗
    Masalliqlar: 🍱

Sabzi – 1 dona
Pomidor – 1 dona
Bodring – 1 dona
Karam – 200 g
Sarimsoqpiyoz – 1 dona
Ko‘kat (shivit, petrushka) – 0.5 bog‘
Zaytun yog‘i – 2 osh qoshiq
Tuz – ta’bga ko‘ra

Tayyorlash bosqichlari: 🍱

1. Masalliqlarni tayyorlash:
Sabzi, pomidor, bodring, ko‘kat va karamni somoncha shaklida to‘g‘rab oling.
Sarimsoqpiyozni mayda maydalang.

2. Karamni ishlov berish:
Karamga tuz qo‘shib, qo‘l bilan yengil g‘ijimlang, bu uning yumshoq va suvli bo‘lishiga yordam beradi.

3. Salatni aralashtirish:
Barcha tug‘ralgan masalliqlarni bir idishga soling.
Ustidan zaytun yog‘i qo‘shib, yengil aralashtiring.

4. Taqdimot:
Salatni likopchaga solib, ta’bga ko‘ra bezang va dasturxonga tortiq qiling.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_olivye": """Olivye salat 🥗
    Masalliqlar: 🍱

O‘rtacha kattalikdagi qaynatilgan kartoshka – 4 dona
Sabzi – 1 dona
Yaxshilab qaynatilgan tuxum – 4 dona
“Doktorskaya” kolbasasi – 300 g
Tuzlangan bodring – 3 dona
Konservalangan yashil no‘xat – 1 banka (200 g)
Mayonez – 200–300 g
Xohishga ko‘ra petrushka va shivit barglari
Tuz va murch – ta’bga ko‘ra

Tayyorlash usuli: 🍱

1. Tayyorlash jarayoni:
Sabzi va kartoshkani yaxshilab qaynatib oling.
Tuxumni ham qaynatib, sovuting.

2. To‘g‘rash:
Tuxum, kartoshka, kolbasa va sabzini bir xil kubik shaklida to‘g‘rang.
Tuzlangan bodringni to‘g‘rab, suyuqligini siqib oling, bu salatda suyuqlik ko‘payib ketmasligini ta'minlaydi.

3. Aralashtirish:
Barcha masalliqlarni aralashtirish uchun katta idishga soling.
Yashil no‘xatni bankadan olib, suvidan ajratib, qo‘shing.

4. Ziravorlar va yakuniy aralash:
Ta’bga ko‘ra tuz va murch seping.
Ustidan mayonez solib, yaxshilab aralashtiring.

5. Sovutish:
Tortiq qilishdan avval salatni 1 soat sovutgichda tindirib qo‘ying.

6. Taqdimot:
Likopchaga solib, ustini shivit yoki petrushka barglari bilan bezang va dasturxonga tortiq qiling.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_tovuqiolivye": """Tovuqli olivye 🍗🥗
    Masalliqlar: 🍱

Tovuqning to‘sh go‘shti – 1 dona
Kartoshka – 3–4 dona
Sabzi – 1 dona
Tuxum – 3 dona
Yangi uzilgan bodring – 1 dona
Tuzlangan bodring – 4–5 dona
Konservalangan yashil no‘xat – 1 banka
Mayonez – 4 osh qoshiq
Tuz va murch – ta’bga ko‘ra

Tayyorlash usuli: 🍱

1. Sabzavotlarni qaynatish:
Kartoshka va sabzini oldindan qaynatib qo‘ying, sabzavotlar yaxshi sovishi uchun.
Qaynatilayotgan suvga tuz qo‘shish kerak, bu sabzavotlarni mazaliroq qiladi.

2. Tozalash va tayyorlash:
Kartoshka, sabzi va tuxumni po‘stidan tozalang.

3. To‘g‘rash:
Barcha masalliqlarni no‘xat kattaligida kubik shaklida to‘g‘rang va chuqurroq idishga soling.

4. Bodringni tayyorlash:
Yangi va tuzlangan bodringlarni po‘stidan tozalab, mayda kubik shaklida to‘g‘rang. Bodringlarni masalliqlar aralashmasiga qo‘shing.

5. Tovuqni tayyorlash:
Tovuq to‘shchasini tuzli suvda qaynatib oling.
Sovugach, uni avval ko‘ndalangiga, keyin uzunasiga kesib, kubik qilib to‘g‘rang. Tovuq bo‘laklarini idishga qo‘shing.

6. Aralashtirish va saqlash:
Barcha masalliqlarni yaxshilab aralashtiring. Agar salatni darhol tortiq qilmasangiz, idishning ustini oziq-ovqat plyonkasi bilan yopib, sovutgichga qo‘ying.

7. Mayonez qo‘shish:
Mayonezga bir chimdim tuz va murch qo‘shib, salatga dasturxonga tortishdan oldin aralashtiring.

8. Bezatish va tortiq qilish:
Salatni chiroyli tortiq qilish uchun maxsus halqachalar ichiga solib, likopchaga qo‘ying.
Ustini ko‘katlar bilan bezang.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_bodringsalat": """Gurunch va bodringli salat 🥗
    Masalliqlar: 🍱

300 gramm mol go‘shti
150 gramm guruch
Bir nechta ko‘k piyoz shoxchalari
2 ta bodring
2 ta tuxum
3-4 osh qoshiq Provansal Premium Gold mayonezi

Tayyorlash usuli: 🍱

1. Tayyorlash:
Mol go‘shti, guruch va tuxumni qaynatib, sovutib qo‘ying.

2. To‘g‘rash:
Tuxum, bodring va mol go‘shtini mayda to‘rtburchak shaklida to‘g‘rang.
Ko‘k piyozni mayda to‘g‘rab oling.

3. Aralashtirish:
Barcha masalliqlarni katta idishga solib, mayonez qo‘shing.

4. Bezash:
Yaxshilab aralashtiring.
Dasturxonga tortishdan oldin ustiga ko‘k piyoz sepib bezang.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_shanxay": """Shanxaycha salat 🥗
    Masalliqlar: 🍱

200 gramm qaynatilgan mol go‘shti
150 gramm qaynatilgan guruch
100 gramm qaynatilgan sabzi
4 ta qaynatilgan tuxum
200 gramm konservalangan yashil no‘xot
1 bog‘ ko‘k piyoz
Ta’bga ko‘ra tuz
150-200 gramm mayonez

Tayyorlash usuli: 🍱

Go‘shtni tayyorlash:
Go‘shtni tuzli suvda pishirib, sovutib oling.

Tuxumni tayyorlash:
Tuxumni yaxshilab qaynatib, sovutib, po‘stidan tozalang.

Sabzi va guruchni qaynatish:
Sabzi va guruchni qaynatib tayyorlab oling.

To‘g‘rash:
Go‘sht, sabzi va tuxumni o‘rtacha to‘rtburchak shaklida to‘g‘rang.
Ko‘k piyozni mayda qilib to‘g‘rang.

Aralashtirish:
Barcha masalliqlarni idishga soling.
Yashil no‘xot, tuz va mayonez qo‘shib, yaxshilab aralashtiring.

Yoqimli ishtaha!🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qushuyali": """Qush uyali salat 🥗
    Masalliqlar: 🍱

Kartoshka – 3 dona
Kungaboqar yog‘i – 1 osh qoshiq
Tuxum – 2 dona
Tuz – ta’bga ko‘ra
Tuyilgan qora murch – ta’bga ko‘ra
Smetana – 150 gr
Shampinion – 70 gr
Tovuq boldiri – 2 dona
Bedana tuxumi – 6 dona
Marinadlangan bodring – 40 gr
Dudlangan kurka go‘shti – 100 gr

Tayyorlash usuli: 🍱

Qo‘ziqorinlarni qovurish:
Shampinionlarni o‘rtacha kattalikda to‘g‘rang.
Tovaga 1 osh qoshiq yog‘ solib, qovuring va sovutib qo‘ying.

Kartoshkani qovurish:
Kartoshkani juda ingichka somoncha shaklida to‘g‘rang.
Qizdirilgan qozonda qovurib, oltinrang tusga kirguncha pishiring.
Pishgan kartoshkani sovuting.

Masalliqlarni tayyorlash:
Tovuq filesini qaynatib, mayda to‘g‘rang.
Marinadlangan bodring va dudlangan go‘shtni somoncha shaklida to‘g‘rang.
Tuxumni qaynatib, mayda bo‘laklarga bo‘ling.

Salatni aralashtirish:
Katta idishda qaynatilgan tuxum, qovurilgan qo‘ziqorin, tovuq go‘shti, dudlangan go‘sht va bodringni birlashtiring.
Tuz va murch qo‘shib, yaxshilab aralashtiring.

Sosni tayyorlash:
Smetana va xantalni birlashtirib, yaxshilab aralashtiring.
Tayyor sosni salatga quying va yaxshilab aralashtiring.

Bezatish:
Tayyor salatni likopcha o‘rtasiga joylashtiring.
Atrofini qovurilgan kartoshka bilan bezang, tuxum uyasiga o‘xshash shakl yarating.
Salat o‘rtasiga qaynatilgan bedana tuxumlarini joylashtiring.

Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_toshkentsalat": """Toshkentcha salat🥗
    Masalliqlar: 🍱

Mol go‘shti – 60 gr
Piyoz – 40 gr
Tuxum – 1 dona
Turp – 40 gr
Mayonez – 40 gr
Tuz va murch – ta'bga ko'ra

Tayyorlash usuli: 🍱

Masalliqlarni tayyorlash:
Turpni somoncha shaklida mayda qilib to‘g‘rang. Uni 10-15 daqiqa davomida muzdek suvga solib qo‘ying, bu uning achchiqligini kamaytiradi.
Piyozni yarim halqa shaklida to‘g‘rang va qovurib oling.

Go‘shtni tayyorlash:
Mol go‘shtini qaynatib, somoncha shaklida to‘g‘rang.
Istasangiz, go‘shtni piyoz bilan birga qovurishingiz ham mumkin.

Tayyorlash:
Idishga qaynatilgan yoki qovurilgan go‘sht, qovurilgan piyoz va muzdek suvdan chiqarilgan turpni soling.
Mayonez qo‘shing, tuz va murch seping. Barchasini yaxshilab aralashtiring.

Bezatish:
Salatni likopchaga solib, ustiga mayda qirg‘ichdan o‘tkazilgan qaynatilgan tuxumni seping.
Yoqimli ishtaha! 🍽😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_portobello": """Portobello salati🥗
    Masalliqlar:🍱

Pomidor – 100 gr
Tuz – ta'bga ko‘ra
Tuyilgan qora murch – ta'bga ko‘ra
Shampinion (yoki boshqa qo‘ziqorin) – 150 gr
Mayonez – 2-3 osh qoshiq
Salat bargi – 1 bog‘
Tuzlangan syomga baliq – 150 gr
Parmesan pishlog‘i – 100-150 gr

Tayyorlash usuli:🍱

Qo‘ziqorin tayyorlash:
Qo‘ziqorinlarni yaxshilab yuvib, mayda qilib to‘g‘rang. Marinadlangan qo‘ziqorin ishlatsangiz, uning suvini to‘kib tashlang.

Ko‘kat va pomidor tayyorlash:
Salat barglarini va pomidorlarni sovuq suvda yaxshilab yuving.
Salat barglarini yirik qilib bo‘laklarga ajrating yoki qo‘lda mayda bo‘laklarga yulib oling.
Pomidorlarni mayda kubik shaklida to‘g‘rang.

Baliqni tayyorlash:
Tuzlangan syomga baliqni mayda bo‘laklarga bo‘ling.

Aralashtirish:
Idishga qo‘ziqorin, salat barglari, pomidor, va baliqni soling.
Parmesan pishlog‘ini mayda qirg‘ichdan o‘tkazib qo‘shing.

Tayyorlash:
Masalliqlar ustiga mayonez qo‘shing, ta'bga ko‘ra tuz va murch seping.
Barchasini yaxshilab aralashtiring.

Tortiq qilish:
Salatni dasturxonga tortiq qilishdan avval 10-15 daqiqaga tindirib qo‘ysangiz, yanada mazali bo‘ladi.

Maslahatlar:
Mayonez o‘rniga smetana ishlatib ko‘ring, salat yengilroq bo‘ladi.
Yoqimli ta'm uchun maydalangan sarimsoqpiyoz qo‘shishingiz mumkin.
Qo‘ziqorin tanlashda o‘zingizga yoqqanini ishlating.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_ananas": """Ananas va tovuqli salat 🍍🍗
    Masalliqlar: 🍱

200 gramm qaynatilgan tovuq filesi
200 gramm pishloq
1 dona konservalangan ananas
1 dona konservalangan makkajo'xori
300 gramm olma
250-300 gramm mayonez

Tayyorlash usuli:🍱

Tovuq tayyorlash:
Tovuq filesini tuzli suvda qaynatib, sovutib oling.

Masalliqlarni to‘g‘rash:
Pishloq, olma va qaynatilgan tovuq filesini 0,7-1 sm kattalikdagi kub shaklida to‘g‘rang.
Ananasni suvidan to‘kib tashlang va halqalarini o‘rtacha kattalikda to‘g‘rang.

Aralashtirish:
Idishga tovuq, pishloq, olma, ananas va makkajo‘xorini soling.
Ustiga mayonez qo‘shib, barchasini yaxshilab aralashtiring.

Tortiq qilish:
Tayyor salatni likopchalarga joylashtiring. Istasangiz, ustiga ko‘katlar yoki mayda maydalangan yong‘oq bilan bezatishingiz mumkin.

Maslahatlar:
Agar salatni yengilroq qilishni istasangiz, mayonezni smetana bilan almashtirishingiz mumkin.
Ta’mga o‘zgacha o‘lcham qo‘shish uchun maydalangan yong‘oq yoki uzum qo‘shishingiz mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_sezar": """Sezar salat 🥗
    Masalliqlar:🍱

Salat uchun:
Tovuq filesi – 400 g
Aysberg salati – 1 bosh
Cherri pomidorlari – 200 g
Parmezan pishlog’i – 100 g
Oq non – yarimta
Sarimsoq – 2 tishcha
Zaytun moyi – 3 osh qoshiq
Tuz, murch – ta’bga ko’ra

Sousi uchun:
Tuxum – 2 dona
Zaytun moyi – 60 ml
Xantal – 2 choy qoshiq
Limon sharbati – 3 osh qoshiq
Sarimsoq – 2 tishcha
Parmezan pishlog’i – 50 g
Tuz – ta’bga ko’ra

Tayyorlash usuli:🍱

Sousni tayyorlash:
Tuxumlarni qaynoq suvda 1 daqiqa ushlab, xona haroratida sovuting. Blender idishiga tuxumlarni chaqib soling.
Sarimsoqni ezib, limon sharbati va mayda qirg‘ichdan o‘tkazilgan parmezan qo‘shing.
Zaytun moyi, xantal va tuzni solib, bir xil massa hosil bo‘lguncha blenderda aralashtiring.

Salatni tayyorlash:

Non suxarigi tayyorlash:
Oq nonning ustki qavatini olib tashlab, kubik shaklida to‘g‘rang.
Sarimsoqni ezib, zaytun moyiga qo‘shing va non ustiga surting.
Non bo‘laklarini 180 °C qizdirilgan pechda 10-15 daqiqa davomida qovuring.

Tovuqni tayyorlash:
Tovuq filesini tuz va murch bilan aralashtirib, o‘rtacha olovda ikkala tomonini oltin rang tusga kirguncha qovuring.
Qovurilgan tovuqni mayda bo‘laklarga bo‘ling.

Aysberg va boshqa masalliqlar:
Aysberg barglarini qo‘lda katta bo‘laklarga ajratib, yaxshilab yuvib quriting.
Cherri pomidorlarini teng ikkiga bo‘ling.
Parmezan pishlog‘ini yupqa plastinkalar shaklida kesing.

Salatni terish:
Likopchaga Aysberg barglarini joylashtiring.
Ustiga tovuq bo‘laklarini qo‘ying.
Keyingi qavatga suxariklar va pomidorlarni joylashtiring.
Parmezan plastinkalarini terib, ustiga sousni quying.

Maslahatlar:
Agar Aysberg yo‘q bo‘lsa, Pekin karamidan foydalanishingiz mumkin.
Tayyor sarimsoqli suxariklar ham ishlatilishi mumkin, lekin uyda tayyorlanganlari mazaliroq chiqadi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_bodringkaram": """Bodring va karamli salat 🥗
    Masalliqlar: 🍱

500 gramm karam
300 gramm bodring
1 bog‘ shivit
1-2 tishcha sarimsoqpiyoz
2 osh qoshiq o‘simlik yog‘i
1 osh qoshiq limon sharbati
0.5 choy qoshiq shakar
Ta'bga qarab tuz va murch

Tayyorlash usuli: 🍱

Qadam 1:
Karamni yupqa somoncha shaklida to‘g‘raymiz va kattaroq idishga solamiz.

Qadam 2:
Karamga tuz va shakar sepib, qo‘llar yordamida yengil ezamiz. Bu karamni yanada yumshoq va shirinroq qiladi.

Qadam 3:
Bodringni somoncha shaklida to‘g‘rab, karam ustiga qo‘shamiz.

Qadam 4:
Shivitni mayda to‘g‘raymiz va sabzavotlar ustiga solamiz.

Qadam 5:
Alohida idishda o‘simlik yog‘i, maydalangan sarimsoqpiyoz, limon sharbati va qora murchni aralashtirib sous tayyorlaymiz.

Qadam 6:
Sousni sabzavotlarga quyib, yaxshilab aralashtiramiz.

Qadam 7:
Tayyor salatni dasturxonga tortamiz.

Maslahatlar:
Ushbu salatga yashil no‘xat, makkajo‘xori yoki pomidor qo‘shib, ta’mini boyitishingiz mumkin.
Salatni sovutgichda 10-15 daqiqa tindirsangiz, yanada mazali bo‘ladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    # --------- PISHIRIQ / PISHIRIQLAR BO‘LIMI ---------
    "dish_turkchaburek": """Turkcha burek  🥠
     Masalliqlar:🍱
• Piyoz – 1 dona
• Kartoshka – 4-5 dona
• Brinza – 400 g
• Smanoql (ismaloq) – 500 g
• Margarin – eritilgan, hamirga surtish uchun
• Ziravorlar: paprika, tuz, zira (qiyma uchun)
• Tayyor hamir yoki uyda qilingan yupqa hamir

Tayyorlash usuli:🍱
1. Qiymalarni tayyorlash:
   - Piyozni mayda to‘g‘rab, qiymani qovurib tayyorlab oling.
   - Qovurilgan qiymadan chiqqan yog‘ga qirg‘ichdan chiqarilgan kartoshkani solib, ozgina paprika qo‘shing. Suv qo‘shib, kartoshkani dimlab pishiring.
   - Smanoqlni yaxshilab yuvib, mayda to‘g‘rab, alohida qovuring.
   - Brinzani maydalab, qovurilgan smanoql bilan aralashtiring.

2. Hamirni o‘rash:
   - Tayyorlangan yupqa hamirni yoyib, ustiga eritilgan margarin surtib chiqing.
   - Har bir qiymadan bir qavat qilib, rulet shaklida o‘rab chiqing.

3. Birinchi bosqich ruletlar:
   - 4 xil qiymadan alohida rulet tayyorlang: biri qiymali, biri kartoshkali, biri smanoqli, biri brinzali.

4. Birlashtirish:
   - Yana uch qavat hamirni yoyib, orasiga margarin surtib qo‘shing.
   - 4 xil ruletni bu uch qavatli hamirning ustiga joylashtiring va yana rulet qilib o‘rang.

5. Sovutish:
   - Tayyor ruletlarni muzxonaga 2-3 soatga qo‘ying.

6. Kesish va pishirish:
   - Muzxonadan olib, ruletlarni ikki barmoq qalinlikda kesing.
   - Ustiga tuxum sarig‘ini surtib, pishirish listiga joylang.

7. Pishirish:
   - Oldindan qizdirilgan 200°C pechda usti qizarguncha pishiring.

Tavsiya:🤗
   - Har bir burak ichida boshqa mazali qiymaning bo‘lishi sizga va mehmonlaringizga turli xil lazzatlarni his qilish imkonini beradi.
   - Ushbu usul mehmon kutish uchun ajoyib variant hisoblanadi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_goshtlisomsa": """Go’shtli somsa  🥟
     Masalliqlar:🍱
• Qatlamli xamir – 500 g
• Qo‘y yoki mol go‘shti – 600 g
• Piyoz – 2 dona
• O‘simlik yog‘i – 2 osh qoshiq
• Qora qalampir – ta'bga ko‘ra
• Tuz – ta'bga ko‘ra
• Tuxum – surtish uchun
• Kunjut va sedana – 1 osh qoshiq

Tayyorlash usuli:🍱
1. Qiymani tayyorlash:
   - Go‘shtni kichik bo‘lakcha shaklida to‘g‘rang yoki qiymalagichdan o‘tkazing.
   - Piyozni mayda kubik shaklida to‘g‘rab, go‘shtga qo‘shing.
   - Tuz, qora qalampir va bir chimdim sedana qo‘shib, yaxshilab aralashtiring.

2. Xamirni tayyorlash:
   - Tayyor qatlamli xamirni taxminan 10x10 sm o‘lchamda bo‘laklarga kesing.
   - Har bir bo‘lakni o‘qlov yordamida yoyib, yupqalashtiring.

3. Somsa tugish:
   - Har bir xamir bo‘lagiga tayyor qiyma soling.
   - Uch burchak shaklida somsa yasab, chetlarini mahkam yopishtiring.

4. Pishirish:
   - Pishirishdan oldin somsalarni pergament qog‘oz bilan qoplangan pishirish listiga tering.
   - Tuxumni ozgina suv bilan aralashtirib, somsalar yuzasiga surting.
   - Kunjut yoki sedana seping.

5. Duxovkada pishirish:
   - Duxovkani 200-215°C darajagacha qizdiring. Somsalarni 20 daqiqa davomida pishiring.
   - Keyin haroratni 170°C darajagacha tushiring va somsalarni yana 10-15 daqiqaga qizartirib pishiring.

6. Xizmat qilish:
   - Tayyor somsalarni dasturxonga issiq holda tortiq qiling.

Maslahatlar:🤗
   - Piyozning miqdorini ko‘proq ishlatsangiz, somsa yanada shirali bo‘ladi.
   - Go‘shtga ozroq yog‘li qism yoki dumba qo‘shish ham yaxshi ta’m beradi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_yupqa": """Yupqa🫔  
     Masalliqlar:🍱
Xamiriga:
• Suv
• Yog‘
• Un
• Tuz
Qiymasiga:
• Tovuq go‘shti – 200 gr
• Piyoz – 2 dona
• Pomidor – 1 dona
• Sarimsoq – 2 bo‘lak
• Ko‘kat va ziravorlar

Tayyorlash usuli:🍱
1. Xamirni tayyorlash:
   - Suvga tuz va yog‘ni qo‘shib aralashtiring.
   - Asta-sekin unni qo‘shib, yumshoq va elastik xamir qorib oling.
   - Xamirni yopib, tindirishga qo‘ying.

2. Qiymani tayyorlash:
   - Tovuq go‘shtini mayda to‘g‘rang.
   - Piyoz va pomidorni to‘rtburchak shaklda, sarimsoqni esa mayda somoncha qilib to‘g‘rang.
   - Qizib turgan yog‘ga avval tovuq go‘shtini solib, qovuring.
   - Sarimsoqni qo‘shing va biroz qovurib, ustidan piyozni soling.
   - Piyoz qizargach, pomidorni qo‘shing va aralashtiring.
   - Hamma masalliqlar yaxshi qovurilgach, tuz, ziravor va mayda to‘g‘ralgan ko‘katlarni solib aralashtiring.

3. Xamirni yoyish va shakllantirish:
   - Tingan xamirni olib, juda yupqa qilib yoying.
   - Yoyilgan xamirni to‘rtburchak shaklda kesib chiqing.
   - Har bir bo‘lakning o‘rtasiga qiymadan solib, xamirni bir tomonidan buklang.
   - Qirralarini yaxshilab yopishtirib, ochilib ketmasligi uchun qattiqroq bosing.

4. Qovurish:
   - Qizib turgan yog‘da yupqalarni solib, ikki tomonini tillarang tusga kirguncha qovuring.

5. Xizmat qilish:
   - Tayyor yupqalarni ta'bga ko‘ra bezatib, issiq holda dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qiymaliquymoq": """Qiymali quymoq🥞 
     Masalliqlar:🍱
• 2 ta tuxum
• 1 osh qoshiq shakar
• 1,5 stakan un
• 2,5 stakan sut
• 2 osh qoshiq o‘simlik yog‘i
• Bir chimdim tuz
• Salat bargi
• Mayonez
• Qiymali ichlik (go‘shtli, sabzavotli, qo‘ziqorinli yoki pishloqli ichlik)

Tayyorlash usuli:🍱
1. Quymoq xamirini tayyorlash:
   - Tuxum va shakarni yaxshilab ko‘pirtiring.
   - Sekin-asta sutni qo‘shib, aralashtiring.
   - Keyin unni qo‘shib, bir hil massa hosil bo‘lguncha aralashtiring.
   - Oxirida tuz va yog‘ni qo‘shib, yana yaxshilab aralashtiring.

2. Quymoqni pishirish:
   - Tayyor xamirni idishdagi (masalan, ketchup yoki mayonez shishasi) joylashtiring. Qopqog‘ida teshik qilib, qizib turgan tovaga xamirni katak shaklida chizib chiqing.
   - Quymoqning bir tomoni qizargach, ehtiyotkorlik bilan aylantirib, ikkinchi tomonini ham pishiring.

3. Ichlikni tayyorlash:
   - Qiymani pishirish uchun avval piyozni qizartirib qovuring.
   - Keyin go‘sht, sabzavot yoki boshqa masalliqlarni qo‘shib, ta'bga ko‘ra tuz va ziravorlar qo‘shib qovuring.

4. Quymoqqa ichlikni qo‘yish:
   - Pishgan quymoqqa salat bargi qo‘ying.
   - Ustiga mayonez va tayyorlangan qiymali ichlikdan soling.
   - Quymoqlarni rulon shaklida o‘rab chiqib, xizmatga tayyorlang.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_pishloqlicheburek": """Pishloqli cheburek  🧀🥟
     Masalliqlar:🍱
• Un – 500 g
• Sut – 250 ml
• Tuz – 15 g (yarim osh qoshiq)
• Pishloq – 500 g
• Pomidor – 1-2 dona
• Kashnich – 1 bog‘

Tayyorlash usuli:🍱
1. Xamir tayyorlash:
   - Un, sut va tuzni aralashtirib, o‘rtacha qattiqlikda xamir qorib oling.
   - Xamirni ustini yopib, 15-20 daqiqaga tindirishga qo‘ying.

2. Ichlikni tayyorlash:
   - Pishloqni qirg‘ichdan chiqarib oling.
   - Kashnichni mayda to‘g‘rab, pishloqqa qo‘shib aralashtiring.
   - Pomidorni mayda kubik shaklida to‘g‘rab, ichlikka qo‘shing.

3. Cheburek tayyorlash:
   - Tingan xamirni 10-12 ta zuvalachaga bo‘lib oling va har birini o‘rtacha yupqalikda yoying.
   - Har bir yoyilgan xamirning o‘rtasiga pishloq, pomidor va kashnichli ichlikni soling.
   - Xamirning bir chetini ikkinchi chetiga bukib, chetlarini qattiq bosib yopishtiring.
   - Maxsus pichoq bilan kesib chiroyli shakl bering yoki sanchqi yordamida chetlarini bosib chiqing.

4. Qovurish:
   - Qizib turgan yog‘da chebureklarning ikki tomonini tilla rang tusga kirguncha qovuring.
   - Tayyor chebureklarni qog‘oz sochiq ustiga qo‘yib, ortiqcha yog‘dan halos qiling.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_gumma": """Gumma 🥠
     Masalliqlar:🍱
Qiymasi uchun:
• Qora taloq – 1 dona
• Yurak – 1 dona
• O‘pka – 200 g
• Bo‘yrak – 1 dona
• Charvi yog‘ yoki dumba – 100 g
• Guruch – ta'bga ko‘ra
• Ziravorlar, tuz va dafna (lavr) yaprog‘i

Xamiri uchun:
• Un – 1 kg
• Suv yoki sut – 600 ml
• Tuz – 1 osh qoshiq
• Xamirturush (droja) – 10 g
• O‘simlik yog‘i – 700 ml

Tayyorlash usuli:🍱
1. Xamirni tayyorlash:
   - Un, suv yoki sut, tuz va xamirturushdan yumshoq xamir qorib oling.
   - Ustini yog‘lab, iliq joyda 1 soatga oshirish uchun qoldiring. Suv yoki sutni iliqroq qilinsa, xamir tezroq oshadi.

2. Qiymani tayyorlash:
   - Charvi yog‘, qora taloq, o‘pka, buyrak va yuraklarni yaxshilab tozalang va iliq suvda bir necha marta yuving.
   - Mahsulotlarni qiymalagichdan o‘tkazing.
   - Qozonga ozgina yog‘ solib, qiymani past olovda qovuring.
   - Tuz, ziravorlar va dafna yaprog‘ini qo‘shib, aralashtiring va dimlab pishiring.
   - Guruchni alohida qaynatib, pishirib oling.
   - Tayyor guruchni qiymaga qo‘shib aralashtiring va ta'bga ko‘ra tuzini rostlang.

3. Gummani shakllantirish:
   - Oshgan xamirdan 50-55 grammlik zuvalachalar uzib, 10-15 daqiqa tindiring.
   - Har bir zuvalachani yoyib, ichiga bir osh qoshiqdan qiymani soling va dumaloq shaklda tuging.
   - Tugilgan qismi pastda bo‘ladigan qilib yog‘langan idishga joylang va 5-6 daqiqa tindiring.

4. Pishirish:
   - Yog‘ni chuqurroq qozon yoki tovaga qizdiring.
   - Gummani tugilgan tomoni pastda bo‘lishiga e'tibor qaratib, qizib turgan yog‘da oltin tusga kirguncha pishiring.

5. Tortish:
   - Pishgan gummalarni ortiqcha yog‘dan halos qilish uchun qog‘oz sochiq ustiga qo‘ying.
   - Tayyor gummani achchiq sous yoki qaynoq choy bilan dasturxonga tortiq qiling.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_pahlava": """Pahlava  
     Masalliqlar:
Xamiri uchun:
• Un – 600-650 gr
• Tuxum sarig‘i – 5 ta
• Qaymoq yoki smetana – 220-240 gr
• Sariyog‘ – 100-120 gr
• Sut – 100 ml
• Shakar – 200 gr
• Tuz va soda – bir chimdimdan

Ichiga:
• Tuxum oqi – 7 ta
• Shakar – 400 gr
• Yong‘oq (maydalangan) – 250 gr
• Mayiz – 250 gr

Ustiga:
• Tuxum sarig‘i – 2 ta
• Yong‘oq (yarimta bo‘lagi) – 15-20 dona
• Asal – 100 gr

Tayyorlash usuli:
1. Xamirni tayyorlash:
   - Xamir uchun masalliqlarni idishga soling, sariyog‘ni eritib qo‘shing.
   - O‘rtacha qattiqlikdagi xamir qorib, ikkita kichik va ikkita katta zuvalalarga bo‘ling.
   - Zuvalalarni 20-30 daqiqaga tindirib qo‘ying.

2. Oraliq qavatlarni tayyorlash:
   - Ikkita kichik zuvalani yoyib, dimxonada juda qizartirmay pishirib oling.
   - Katta zuvalalardan biri pastki, biri yuqori qatlam uchun ishlatiladi.

3. Ko‘pik tayyorlash:
   - Tuxum oqini shakar bilan mikserda qattiq ko‘pik holatiga kelguncha ko‘pirtiring (idishni ag‘darganda oqib ketmasligi kerak).
   - Tayyorlangan ko‘pikni sovuqligini saqlash uchun muzlatgichga qo‘ying.

4. Pahlavani qatlamlash:
   - Katta zuvaladan birini patnisga yoyib qo‘ying (patnisni yog‘lab oling).
   - Xamirga ko‘pikning uchdan bir qismini surting, ustiga maydalangan yong‘oq va mayiz seping.
   - Oraliq qavatlarga pishirilgan kichik zuvalalarni qo‘ying, har bir qavatga ko‘pik, yong‘oq va mayiz surting.
   - Eng yuqori qatlam uchun katta zuvalani yoyib, ustiga qo‘ying.

5. Pishirish:
   - Ustiga tuxum sarig‘ini surting va romb shaklida kesib chiqing.
   - Har bir rombning o‘rtasiga yong‘oq mag‘zi qo‘ying.
   - 180-200 darajali dimxonada tillarang tusga kirguncha pishiring.

6. Tayyorlash:
   - Pishgan pahlavaning ustiga isitilgan asal surting.
   - Oldindan kesilgan romb bo‘yicha kesib chiqing.
   - Tayyor pahlavani ta'bga ko‘ra bezab, dasturxonga tortiq qiling.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_chakchak": """Chak-chak  🍯
     Masalliqlar:🍱
• Tuxum – 4 ta
• Mayonez – 1 osh qoshiq
• Un – 300-350 gr
• Tuz – 1 chimdim
• Soda – ozgina
• Uksus – sodani eritish uchun
• O‘simlik yog‘i – 600 gr
• Asal – 1 stakan
• Shakar – 2 stakan
• Suv – 2 stakan

Tayyorlash usuli:🍱
1. Xamir tayyorlash:
   - 4 ta tuxum, 1 osh qoshiq mayonez, soda (uksus bilan bijitilgan), va bir chimdim tuzni idishga solib mikser yordamida ko‘pirtiring.
   - Asta-sekin un qo‘shib, yumshoq xamir qoring. Xamirni tindirib qo‘ying.

2. Xamirni tayyorlash va kesish:
   - Tingan xamirni yoying va 3-4 sm kenglikdagi lentalarga kesing.
   - Har bir lentani gugurt cho‘piday ingichka qilib to‘g‘rab, unlab qo‘ying.

3. Qalamchalarni pishirish:
   - Qizdirilgan yog‘da qalamchalarni tilla rangga kirguncha pishiring.
   - Yog‘ juda issiq bo‘lmasin, aks holda qalamchalar yorilib ketishi mumkin. Pishgan qalamchalar yumshoq va og‘izda eriydigan bo‘lishi kerak.

4. Qiyom tayyorlash:
   - Ikki stakan shakar va ikki stakan suvni qaynating.
   - Qiyomni stakandagi sovuq suvga tomizib tekshiring: agar tomchi suvga aralashmay tagiga cho‘ksa, qiyom tayyor.
   - Qiyom tayyor bo‘lgach, asalni qo‘shib bir marta qaynating.

5. Aralashtirish va shakllantirish:
   - Qiyomni biroz sovuting va qalamchalarni qiyom bilan yaxshilab aralashtiring.
   - Ta’bga ko‘ra mayiz, yong‘oq yoki kunjut qo‘shishingiz mumkin.

6. Shakl berish:
   - Aralashmani idishga solib, bosib chiqib shakllantiring yoki alohida bo‘laklar hosil qiling.
   - Chak-chakni 2-3 soatga tindirib qo‘ying.

7. Tortiq qilish:
   - Tayyor chak-chakni bo‘laklarga bo‘lib, likopchaga joylashtiring va ta’bga ko‘ra bezating.

Maslahat: 🤗
Qiyomni aralashtirish paytida qo‘llaringiz va idish yopishib qolmasligi uchun ozgina o‘simlik yog‘idan foydalansangiz bo‘ladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_turkchapishiriq": """Turkcha pishiriq🥮
     Masalliqlar:🍱
• 1 o'ram Yufka xamiri
• 300 gramm brinza
• 100 gramm qattiq pishloq
• 50 millilitr sut
• 1 dona tuxum
• Qovurish uchun o'simlik yog'i
• 1 bog' shivit
• 1 bog' petrushka

Tayyorlash usuli:🍱
1. Sut va tuxum aralashmasi:
   - Tuxumni idishga chaqib soling va sanchiq yordamida ko'pirtiring.
   - Ustidan sutni qo'shing va yaxshilab aralashtiring.

2. Ichlikni tayyorlash:
   - Brinza va qattiq pishloqni qirg'ichdan o'tkazing.
   - To'g'ralgan shivit va petrushkani qo'shib, yaxshilab aralashtiring.

3. Xamirni tayyorlash:
   - Tayyor yufka xamirini to'rt teng bo'lakka bo'ling.

4. Xamirni to'ldirish:
   - Har bir xamir bo'lagining o'rtasiga 4 osh qoshiq ichlik qo'ying.
   - Xamirning bir tomoniga tuxumli aralashmadan surtib, ichlik ustidan yopib chiqing.
   - Qarama-qarshi tomoniga ham tuxumli aralashmadan surtib, ustidan yopib chiqishni davom ettiring.
   - Shu usulda qolgan tomonlarni ham buklab yopib chiqing.

5. Pishirish:
   - Qizdirilgan tovada o'simlik yog'ini soling.
   - Tayyorlangan Go’zlemeni chokli tomoni bilan tovaga qo'ying va past olovda qovuring.
   - Keyin ag'darib, orqa tomonini ham qizartiring.

6. Tortiq qilish:
   - Tayyor Go’zlemeni issiqligida dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qozonsomsa": """
     Qozon somsa🥟
Masalliqlar:🍱
Hamiriga:
1. 500 ml tuzli suv
2. 6 piyola un
3. 80% li margarin
4. 2 osh qoshiq oq yog’

Tayyorlash usuli:🍱
1. Xamirni tayyorlash:
   - Tuzli suvni idishga quyib, unni asta-sekin qo'shib yumshoq xamir qorib oling.
   - Xamirni 20 daqiqa dam olib tindiring.
   - Margarin va oq yog'ni eritib, xamirni yoyib surting va bir necha qatlam qilib taxlang. Keyin xamirni yana bir necha daqiqa tindiring.

2. Somsa tugish:
   - Xamirni teng bo’laklarga bo’lib, har birini alohida yoying.
   - Somsa ichiga o'zingiz xohlagan qiymadan (masalan, go'sht va piyozli) soling.
   - Somsa shaklida tugib chiqing.

3. Yopishtirish va pishirish:
   - Tayyor somsalar ustiga tuxum sarig’ini surtib, kunjut seping.
   - Qizdirilgan qozon ichiga somsalarni joylashtirishdan oldin, tagiga tuxum oqini surtib, qozonning devorlariga yopishtiring.

4. Pishirish:
   - Qozonni qopqog’ini yopib, baland olovda 15 daqiqa davomida pishiring.
   - So’ng olovni pasaytirib, somsalarni yana 40 daqiqaga qoldiring.
   - Agar usti qizarmasa, somsalarni olib, pechda usti tillarang tusga kirguncha pishiring.

5. Tortiq qilish:
   - Qozon somsalarini issiqligida dasturxonga torting. Mazasi tandir somsaga yaqin bo'lib chiqadi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_sabzavotlisomsa": """
     Sabzavotli somsa🥟
Masalliqlar:🍱
• Xamir uchun:
  Somsa xamiri (ikkinchi usul)
• Ichlik uchun:
  Piyoz – 1–2 dona (300–400 gr)
  Rangli bulg‘ori (qizil, yashil yoki sariq) – 2 dona (500–600 gr)
  Pomidor – 2 dona (200 gr)
  Charvi yog‘ – 200 gr
  Go‘sht – 100 gr
  Tuz va ziravorlar – ta’bga ko‘ra

Tayyorlash usuli:🍱
1. Ichlikni tayyorlash:
   - Piyoz, bulg‘ori, pomidor, go‘sht va charvi yog‘ni bir xil mayda kubik shaklida to‘g‘rang.
   - Barcha masalliqlarni aralashtirib, tuz va ziravorlar qo‘shib qiyma tayyorlang.

2. Xamirga shakl berish:
   - Xamirni yoyib, o‘rtasiga qiyma soling.
   - Xamirni chetlardan bukib, dumaloq shakl hosil qiling.

3. Pishirishga tayyorlash:
   - Dumaloq shaklda tugilgan somsalar ustiga tuxum surting.
   - Ta’bga ko‘ra, ustiga sedana yoki kunjut sepib chiqing.

4. Pishirish:
   - Duxovkani 180 darajaga qizdiring.
   - Somsalarni dimxonaga qo‘yib, 22–24 daqiqa davomida usti qizarguncha pishiring.

5. Tortiq qilish:
   - Pishgan somsalarni likopchalarga terib, issiq holda dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_yuraksomsa": """Yurak somsa 🥟
     Masalliqlar:🍱
• Xamir:
  Somsa xamiri (birinchi usul)
• Ichlik uchun:
  Go‘shtning yog‘li qismi – 300 gr
  Agar go‘sht yog‘siz bo‘lsa – 100 gr charvi yog‘i
  Piyoz – 300 gr
  Tuz va ziravorlar – ta’bga ko‘ra

Tayyorlash usuli:🍱
1. Ichlikni tayyorlash:
   - Piyoz, go‘sht va charvi yog‘ni mayda kubik shaklida to‘g‘rang.
   - Tuz va ziravorlar qo‘shib, qiyma tayyorlang.

2. Xamirni tayyorlash:
   - Somsa xamiridan taxminan 50 grammlik kubik bo‘lakchalar kesib oling.
   - Har bir xamir bo‘lakchasini juva yordamida yoyib chiqing.

3. Somsa tugish:
   - Yoyilgan xamirning o‘rtasiga bir osh qoshiqdan qiyma soling.
   - Xamirni uchburchak shaklida tuging va ikki pastki qismini chetlarini bukib qo‘ying.
   - Hosil bo‘lgan konus shaklidagi somsani, ikki cheti bukilgan tomonining o‘rtasini ichiga barmoq yordamida bosib, yurak shakliga keltiring.

4. Pishirish:
   - Tayyor bo‘lgan yurak shaklidagi somsalarni dimxona yoki duxovkaga qo‘yishdan avval ustiga tuxum surtib chiqing.
   - Duxovkani 180 darajaga qizdirib, somsalarni 20–25 daqiqa davomida pishiring.

5. Tortiq qilish:
   - Pishgan somsalarni xohishingizga ko‘ra bezatib, issiq holda dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_qatlamasomsa": """Qatlama somsa🥟  
     Masalliqlar:🍱
• Xamir uchun:
  o Un – 1 kg
  o Qatiq – 100 gr
  o Suv – 1 stakan
  o Soda – 1 choy qoshiq
  o Sirka – 1 choy qoshiq
  o Tuz – 2 choy qoshiq
  o Margarin – 250 gr
• Ichlik uchun:
  o Mol go‘shti – 500 gr
  o Piyoz – 300 gr
  o Dumba yog‘ – 150 gr
  o Tuz – ta’bga ko‘ra

Tayyorlash usuli:🍱
1. Xamirni tayyorlash:
   - Qatiqqa sirkada so‘ndirilgan soda qo‘shing va aralashtiring.
   - Tuzli suvga qatiqni qo‘shib, yana aralashtiring.
   - Unni asta-sekin qo‘shib, o‘rtacha qattiqlikda xamir qorib oling.
   - Xamirni 30 daqiqa davomida tindiring.

2. Qatlam hosil qilish:
   - Xamirni yupqa qilib yoyib, eritilgan margarinni surting.
   - Xamirni zich qilib o‘rab, sellofanga o‘rab, 1 sutka davomida muzlatgichda saqlang.

3. Ichlikni tayyorlash:
   - Mol go‘shti, piyoz va dumba yog‘ini mayda to‘g‘rang.
   - Ta'bga ko‘ra tuz sepib, yaxshilab aralashtiring.

4. Somsa tayyorlash:
   - Xamirni muzlatgichdan olib, eritib, mayda zuvalachalarga kesib oling.
   - Zuvalachalarni juvada yoying va markaziga qiyma soling.
   - Somsalarni yumaloq shaklda tugib, ularni to‘rttasini birlashtiring.

5. Pishirish:
   - Somsalarni listga terib chiqib, ustiga tuxum surting va kunjut urug‘i sepib chiqing.
   - Somsalarni 220 darajagacha qizdirilgan gaz pechiga joylashtiring.
   - 10 daqiqadan so‘ng olovni 180 darajagacha pasaytiring va 25 daqiqa davomida pishiring.

6. Bezash:
   - Pishgan somsalarni gaz pechidan olib, ustiga ozgina sovuq suv sachratib yuboring.
   - Bu usul somsalarni yaltiroq va ishtahaochar qiladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    # ----------- SHIRINLIKLAR (SHIRINLIK) BO‘LIMI -----------
    "dish_nisholda": """Nisholda 🍚
     Masalliqlar:🍱
• Shakar – 900 gr
• Tuxum oqsili – 10-12 dona
• Limon kislotasi – 1 gr
• Shirinmiya ildizi qaynatmasi – 10 gr
• Jelatin – 0,5 gr
• Vanilin – 0,1 gr

Tayyorlash usuli:🍱
1. Shirinmiya ildizini qaynatish:
   Shirinmiya ildizini yuvib, tozalang va mayda to‘g‘rang.
   Taxminan 3–4 porsiyali suvda qaynatib pishiring.
   Mis qozonga ildizni 1/3 qismigacha joylashtiring va bug‘ yordamida isitib pishiring.
   Ildiz qaynatilgan suvni elakdan o‘tkazing va filtrlang. Bu jarayonni 2–3 marta takrorlang, har safar suv quyib qaynatib oling.
   Tayyor qaynatmalarni alohida idishga to‘plang.

2. Karamel sharbatini tayyorlash:
   Idishga suv va shakarni soling (1 kg shakarga 300 gr suv) va shakar eriguncha aralashtirib qaynatib oling.
   Qaynayotganda limon kislotasining 2/3 qismini qo‘shing va sharbatning haroratini +112 °C ga yetguncha qaynatib pishiring.
   Tayyor sharbati elakdan o‘tkazing va harorati +55–60 °C gacha sovuting.

3. Ko‘piksimon massa tayyorlash:
   Sovutilgan tuxum oqsillarini mikser yoki qo‘lda 20–25 daqiqa davomida ko‘pirtiring.
   Savalash davomida shirinmiya ildizi qaynatmasini va jelatinni asta-sekin quyib aralashtirishda davom eting.
   Aralashmani yana 7–10 daqiqa savalang, yumshoq va barqaror ko‘pik hosil bo‘lguncha.

4. Sharbatni qo‘shish:
   Ko‘piksimon massaga sovutilgan karamel sharbati sekin-asta quyib, bir xil massa hosil bo‘lguncha aralashtiring.
   Vanilin va qolgan limon kislotasini qo‘shing. Aralashmani yana 10 daqiqa davomida ko‘pirtiring.

5. Servis:
   Tayyor nisholdani chiroyli idishlarga solib, darhol dasturxonga torting yoki sovitib qo‘yishingiz mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_holvetar": """Holvetar 🥣
1-usul ‼️
Masalliqlar:🍱
• Qo‘y yog‘i (eritilgani) – 100 gr
• Un – 1 stakan
• Shakar yoki oq qand – 1 stakan (150 gr)
• Qaynoq suv – 3 stakan

Tayyorlash usuli:🍱
1. Qozonni qizdiring va yog‘ni solib dog‘lab oling. Kapkir bilan shopirib, tobini chiqaring.
2. Yog‘ga unni solib, doimiy aralashtirib turing. Un jigarrang tusga kirib, qizarib pishishi kerak.
3. Qaynoq suvda shakarni eritib, uni qozonga sekin-asta quyib aralashtiring.
4. Qumoqlarni yoyish uchun doimiy ravishda aralashtiring. Olovni sustroq qilib, qizg‘ish rangga kirguncha pishiring.
5. Tayyor holvaytarni olovdan olib, tobini chiqarib, piyolalarga yoki likopchalarga solib dasturxonga torting.

2-usul ‼️
Masalliqlar:🍱
• Bug‘doy uni – 100 gr
• Shakar – 150-200 gr
• O‘simlik yog‘i – 50 gr
• Qaynagan suv – 1 kosa
• Vanilin – 2 gr

Tayyorlash usuli:🍱
1. Tovaga o‘simlik yog‘ini solib, qizdiring (dog‘lang).
2. Tovaga unni solib, doimiy ravishda aralashtirib turing. Un jigarrang tusga kirguncha qovuring.
3. Qaynoq suvda shakarni eritib, vanilinni qo‘shing va sekin-asta qozonga quyib aralashtiring.
4. Muntazam ravishda kavlab turing. Holvaytar quyuqlasha boshlaganda olovdan oling.
5. Tayyor holvaytarni likopchalarga suzib, sovutib dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_tvaroglikr": """Tvarogli krendel 🥣
    Masalliqlar:🍱
Xamiri uchun:
• Un – 300 gramm
• Tvorog – 200 gramm
• Smetana – 2 osh qoshiq
• Shakar – 3 osh qoshiq
• Tuz – 0,5 choy qoshiq
• Tuxum – 2 dona
• Qabartma (razrixlitel) – 1 choy qoshiq
• O‘simlik yog‘i – 2 osh qoshiq

Ustiga sepish uchun:
• Shakar – 2 osh qoshiq
• Vanil shakari – 1 choy qoshiq

Tayyorlash usuli:🍱
1. Un va qabartmani aralashtiring.
   Bir idishda un va qabartmani birlashtirib aralashtiring.

2. Tvorogli massani tayyorlang.
   Alohida idishga tvorog va smetanani solib yaxshilab aralashtiring.

3. Tuxum va shakar qo‘shing.
   Tvorogli massaga shakar, tuz, yog‘ va tuxumni qo‘shib, venchik yordamida yaxshilab aralashtiring.

4. Xamirni tayyorlang.
   Tvorogli massaga unli aralashmani soling va cho‘ziluvchan, qo‘lga yopishmaydigan xamir qorib oling.

5. Xamirni bo‘laklarga bo‘ling.
   Tayyor xamirni taxminan 45 grammdan bo‘laklarga ajrating.

6. Krendel shaklini bering.
   Har bir bo‘lakni semiz bo‘lmagan tasma shaklida yoyib, ikki chetini bir-biriga qaratib, o‘rab kelib, krendel shaklini hosil qiling.

7. Ustiga shakarli aralashma seping.
   Shakarni vanil shakari bilan aralashtiring. Tayyor krendellarni bir tarafini shakarli aralashmaga botiring.

8. Krendellarni pishiring.
   Krendellarni pergament qog‘ozi bilan qoplangan patnisga joylashtiring va 180 °C darajada qizdirilgan gaz pechida 30 daqiqa davomida pishiring.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_shokoglazur": """Shokoladli glazur 🍫
     Masalliqlar:🍱
• Kakao – 4 osh qoshiq
• Shakar – 12 osh qoshiq
• Sut – 8 osh qoshiq
• Sariyog‘ – 50 g
• Vanilin – ta’bga ko‘ra

Tayyorlash usuli:🍱
1. Masalliqlarni tayyorlang.
   Shakar va kakao kukuni bir idishda yaxshilab aralashtiriladi, bir xil bo‘lishi kerak.

2. Sut qo‘shing.
   Aralashmaga iliq sut qo‘shing va yaxshilab aralashtiring.

3. Aralashmani qizdiring.
   Idishni o‘rtacha olovga qo‘yib, shakar erishi va aralashma bir xil konsistensiyaga kelguncha aralashtirib turing.

4. Qaynatib oling.
   Aralashma qaynab chiqqach, darhol olovni o‘chiring va aralashmani sovutishga qo‘ying.

5. Sariyog‘ qo‘shing.
   Sovigan aralashmaga sariyog‘ va vanilin qo‘shing. Sariyog‘ eriguncha yaxshilab aralashtiring.

6. Quyuqlashtiring.
   Glazurni 30 daqiqa davomida xona haroratida qoldiring. Agar juda quyuqlashsa, ozroq suv qo‘shib, olovda biroz qizdirib olishingiz mumkin.

7. Tayyorlash bo‘yicha maslahatlar:
   - Agar glazur yumshoq va havodor chiqishini istasangiz, olovdan olgach, mikser yordamida aralashtiring.
   - Glazur oqib ketmasligi uchun, pishiriq yuzasi sovuq bo‘lishi maqsadga muvofiq.

Tayyor! Glazur turli pishiriqlarni bezash va ta’mini boyitish uchun mukammal.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_bananlieskimo": """Bananli eskimo 🍌
    Masalliqlar:🍱
• Banan – 2 dona
• Yong‘oq – 50 gr
• Sutli shokolad – 100 gr

Tayyorlash bosqichlari:🍱
1. Bananlarni kesib tayyorlang.
   Bananni po‘stlog‘idan ajratmasdan 2-4 bo‘lakka bo‘ling (bananning uzunligiga qarab). Har bir bo‘lakka muzqaymoq cho‘pini tiqing yoki choy qoshiqchadan foydalaning.

2. Po‘stini ajratib muzlatib qo‘ying.
   Po‘stlog‘idan tozalang va bo‘laklarni tarelkaga terib, muzlatgichga 3-4 soatga muzlashi uchun qo‘ying.

3. Yong‘oqlarni maydalang.
   Yong‘oqlarni blender yoki pichoq yordamida maydalang va bir chetga qo‘yib turing.

4. Shokoladni eritib tayyorlang.
   Shokoladni bo‘laklarga bo‘ling va suv bug‘ida bir xil massa hosil bo‘lguncha eriting.

5. Shokoladni surting.
   Muzlagan banan bo‘laklarini muzlatgichdan olib, silikon kistochka yordamida shokoladni har bir banan bo‘lagiga surtib chiqing.

6. Yong‘oqlar bilan bezang.
   Shokolad surtganingizdan so‘ng birdaniga maydalangan yong‘oqlarni ustidan seping.

7. Muzlatib qo‘ying.
   Tayyorlangan banan bo‘laklarini yana 30-60 daqiqaga muzlatgichga qo‘ying.

8. Xizmat qilishdan oldin olib qo‘ying.
   Tanovvul qilishdan 3-5 daqiqa oldin muzlatgichdan olib, yumshashini kuting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_jemlipirog": """Jemli pirog 🥮
    Masalliqlar:🍱
• Un: 400 gramm
• Qabartma (razrixlitel): 10 gramm
• Vanil shakari: 0,5 choy qoshiq
• Sariyog': 200 gramm
• Tuxum: 2 dona
• Shakar upasi: 100 gramm
• Sovuq sut: 2 osh qoshiq
• Rezavor jem: 200 gramm
• Ustiga surtish uchun: 1 dona tuxum

Tayyorlash bosqichlari:🍱
1. Un va qabartmani aralashtiring.
   Elangan unni idishga solib, qabartma va vanil shakarini qo‘shing. Venchik yordamida yaxshilab aralashtiring. Elangan un xamirni yumshoq va havodor qiladi.

2. Sariyog'ni qo‘shing.
   Sovuq sariyog'ni qirg'ichdan o'tkazib, unli aralashmaga qo‘shing. Ularni qo‘l bilan uvoq shakliga keltiring, so'ng shakar upasini aralashtiring.

3. Xamir qorish.
   Unli massaning o‘rtasida chuqurcha hosil qiling. Tuxum va sutni qo‘shib, xamir qorishni boshlang. Xamir biroz quruq ko‘rinsa ham qo‘shimcha sut qo‘shishga shoshilmang – sariyog‘ erib, massani birlashtiradi.

4. Xamirni tindirish.
   Tayyor xamirni yopishqoq plyonka bilan o‘rab, 15 daqiqaga muzlatgichga qo‘ying.

5. Xamirni bo‘lish.
   Muzlatgichdan olib, xamirni ikki qismga bo‘ling. Bir qismi kattaroq bo‘lsin (asos uchun), ikkinchi qismi esa pirog usti uchun ishlatiladi.

6. Asosni tayyorlash.
   Xamirning katta qismini 0,5 sm qalinlikda yoyib, pergament qog‘ozi bilan qoplangan gaz pechi patnisiga joylashtiring. Yonlaridan uzunligi 4 sm, eni 1 sm bo‘lgan tasmalar kesib oling.

7. Jemni soling.
   Pirogning o‘rtasiga jemni solib, yuzasini yaxshilab tekkislang.

8. Panjara tayyorlash.
   Qolgan xamirni ham 0,5 sm qalinlikda yoyib, 1 sm kenglikdagi tasmalar kesing. Tasmalarni pirog ustiga panjara shaklida terib chiqing.

9. Tuxum surting.
   Pirogning ustiga tuxum surtib, chiroyli ko‘rinishi uchun tayyorlang.

10. Pishirish.
   180°C darajagacha qizdirilgan gaz pechida pirogni 25-30 daqiqa davomida pishiring. Usti oltin tusga kirguncha pishishi kerak.

11. Bezatish.
   Sovigan pirogni shakar upasi bilan sepib, xizmat qiling.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_tvoroglibulochka": """Tvorogli bulochka 🥨
     Masalliqlar:🍱
• Tuxum: 2 dona
• Tvorog: 250 gramm
• Shakar upasi: 175 gramm
• Iste'mol sodasi: 0,5 choy qoshiq
• Vanil shakari: 0,5 choy qoshiq
• Tuz: bir chimdim
• Un: 350 gramm
• Yumshatilgan sariyog': 75 gramm
• Ustiga surtish uchun: tuxum
• Shakar upasi: 40 gramm

Tayyorlash bosqichlari:🍱
1. Tvorogni maydalash.
   Tvorogni blender yordamida bir xil konsistensiyaga keltiring.

2. Massani tayyorlash.
   Idishga tuxum, shakar upasi, soda, tuz va vanil shakarini solib, mikser yordamida yaxshilab ko‘pirtiring.

3. Tvorogni qo‘shish.
   Ko‘pirtirilgan massani tvorog bilan aralashtiring. So‘ngra asta-sekin unni qo‘shib, yumshoq xamir qorib oling.

4. Xamirni bo‘lish va yoyish.
   Xamirni teng ikkiga bo‘ling. Har bir bo‘lakni 0,5 sm qalinlikda yoying.

5. Sariyog' va shakar qo‘shish.
   Yoyilgan xamir ustiga yumshatilgan sariyog‘ surting va shakar upasini sepib chiqing. Xamirni rulet shaklida o‘rang.

6. Ruletni bo‘laklarga kesish.
   Ruletni 3-4 sm kenglikdagi bo‘laklarga kesing. Bo‘laklarni pergament qog‘ozi to‘shalgan gaz pechi patnisiga joylashtiring.

7. Pishirishga tayyorlash.
   Bo‘laklar ustiga tuxum surtib, 180°C darajagacha qizdirilgan gaz pechiga qo‘ying. 30 daqiqa davomida pishiring.

8. Bezatish.
   Pishgan bulochkalarga shakar upasini sepib, dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_malinalichizkeyk": """Malinali chizkeyk🍮 
     Masalliqlar:🍱
• Shakar: 200 gr
• Sariyog': 100 gr
• Tuxum: 3 dona
• Tuz: 1/2 choy qoshiq
• Limon sharbati: 1 osh qoshiq
• Kraxmal: 15 gr
• Tvorog: 750 gr
• Pechene: 200 gr
• Slivki (yoki smetana/sut): 100 ml
• Tuxum sarig'i: 2 dona
• Limon po‘stlog‘i: 1 dona
• Malina (yoki boshqa mevalar): ta’bga ko‘ra

Tayyorlash usuli:🍱
1. Asos tayyorlash:
   - Sariyog‘ni mikroto‘lqinli pechda 30 soniya davomida eritib oling.
   - Pechenelarni blender yordamida maydalab, uvoq hosil qiling.
   - Sariyog‘ni pecheneli uvoq bilan aralashtiring.
   - Tayyorlangan aralashmani diametri 20 sm bo‘lgan qolipga bir tekis qilib yoying (qolip tagiga qog‘oz qo‘yishni unutmang). Muzlatgichga qo‘ying.

2. Tvorogli massani tayyorlash:
   - Tvorogli pishloqni mikser yordamida bir xil massa hosil bo‘lgunicha aralashtiring.
   - Shakar, kraxmal, limon po‘stlog‘i va tuz qo‘shib, yaxshilab aralashtiring.
   - Tuxumlarni bittadan solib, har biridan keyin yaxshilab aralashtiring.
   - Oxirida slivki va limon sharbatini qo‘shib, yana aralashtiring.

3. Chizkeykni yig‘ish:
   - Tayyorlangan tvorogli massaning yarmisini muzlatgichdan olingan asos ustiga quying.
   - Ustidan malina yoki boshqa mevalarni taqsimlang.
   - Qolgan tvorogli massani ustiga quying.

4. Pishirish:
   - Duxovkani 200°C darajaga qizdiring va chizkeykni 10 daqiqa pishiring.
   - Haroratni 105°C ga tushiring va yana 30 daqiqa davomida pishiring. Chizkeykning o‘rtasi biroz "qimirlayotgan" bo‘lsa, pishgan hisoblanadi.

5. Sovutish va bezatish:
   - Tayyor chizkeykni xona haroratida sovuting, so‘ng muzlatgichga qo‘yib, 4-5 soat davomida tindiring.
   - Xohishga ko‘ra, ustini malina va boshqa bezaklar bilan bezating.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_bolqaymoq": """Bolqaymoq 🥣
     Masalliqlar:🍱
• Qaymoq: 250 gr
• Asal: 2 osh qoshiq
• Un: 1 choy qoshiq

Tayyorlash usuli:🍱
1. Qaymoqni qizdirish:
   - Qaymoqni past olovda, doimiy qo‘zg‘atib, qizdiring.
   - Asta-sekin asalni qo‘shing va yaxshilab aralashtiring. Asal issiqlikda erib, qaymoq bilan bir hil massa hosil qiladi.

2. Sovutish:
   - Qaymoq va asal aralashmasini olovdan olib, xona haroratida sovuting. Agar xohlasangiz, uni tezroq sovutish uchun muzlatgichga qo‘yishingiz mumkin.

3. Urish va qalinlashtirish:
   - Sovigan aralashmani mikser yoki maxsus urib ko‘taruvchi vosita yordamida yaxshilab urib chiqing.
   - Urayotganda 1 choy qoshiq un qo‘shing va qaymoq qalinlashguncha urishda davom eting.

4. Tayyor bo‘lgan bolqaymoq:
   - Bolqaymoqni non, sevimli mevalaringiz yoki turli pishiriqlar bilan iste’mol qilishingiz mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_murabbolipirog": """Murabboli pirog 🥧
    Masalliqlar:🍱
• Un: 480 gr
• Shakar: 200 gr
• Tuxum: 2 dona
• Soda: 1 choy qoshiq
• Margarin: 200 gr
• Murabbo: 200 gr

Tayyorlash usuli:🍱
1. Aralashmani tayyorlash:
   - Xona haroratida yumshatilgan margarinni shakar bilan mikserda yaxshilab aralashtiring.
   - Tuxumni qo‘shing va yana 5-10 daqiqa davomida aralashtirishda davom eting.

2. Xamirni qorish:
   - Aralashmaga soda va elangan unni qo‘shib, yumshoq xamir qoring.
   - Xamirni ikkiga bo‘lib, bir qismini muzlatgichda 1 soatga qo‘ying.

3. Asosini tayyorlash:
   - Qolipni yog‘lab, xamirning muzlatilmagan qismini yoyib, qolipga soling.
   - Xamir ustiga murabbo surtib chiqasiz.

4. Muzlagan xamirni qo‘shish:
   - Muzlatilgan xamirni qirg‘ichdan chiqarib, murabbo ustiga teng qilib tarqating.

5. Pishirish:
   - Qizdirilgan duxovkada (180 °C daraja) 20-25 daqiqa davomida pishirib oling.

6. Bezash:
   - Tayyor pirogni sovuting va xohishga ko‘ra ustiga shakar upasi sepib bezang.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_asallipirojniy": """Asalli pirojniy 🥧
     Masalliqlar:🍱
Xamir uchun:
• 70 gramm asal
• 150 gramm shakar
• 60 gramm sariyog'
• 2 ta tuxum
• 1 choy qoshiq iste'mol sodasi
• 0,5 choy qoshiq tuz
• 400 gramm un

Krem uchun:
• 400 gramm tvorogli pishloq
• 200 gramm 35 %li yog'li qaymoq
• 150 gramm shakar upasi
• 50 gramm rezavor mevalardan tayyorlangan jem
• Bezak uchun istalgan rezavor mevalar

Tayyorlash usuli:🍱
1. Asalli xamir tayyorlash:
   - Sariyog', asal va shakarni idishga solib, o'rtacha olovda suyulgunicha aralashtirib isitib oling.
   - Tuxumlarni alohida idishda sanchqi yordamida aralashtiring va asalli aralashmaga asta-sekin qo'shib, tez-tez aralashtiring.
   - Soda solib, yana 1 daqiqa davomida aralashtiring (massa ko'piradi — bu normal holat).
   - Olovdan olib, sovuting va tuz bilan aralashtirilgan unni asta-sekin qo'shib xamir qorib oling.
   - Xamirni plyonkaga o'rab, muzlatgichga 2 soatga qo'ying.

2. Korjlarni tayyorlash:
   - Xamirni muzlatgichdan chiqarib, 3-4 bo'lakka bo'ling.
   - Har bir bo'lakni 3 mm qalinlikda yoyib, 7-8 smli doiralar kesib oling.
   - Doirachalarni sanchqi yordamida teshib, 200 °C darajada qizdirilgan gaz pechida 5 daqiqa davomida pishiring.
   - Korjlarni sovutib oling.

3. Krem tayyorlash:
   - Tvorogli pishloq va shakar upasini mikserda bir xil bo'lguncha ko'pirtiring.
   - Qaymoqni qo'shib, massa quyuqlashguncha uring.
   - Tayyor kremni konditer qopchasiga soling.

4. Pirojniylarni yig'ish:
   - Sovigan korjlarni patnisga qo'yib, ustiga krem va jemni doira bo'ylab surting.
   - Ikkinchi korjni qo'yib, yana krem va jem bilan surting.
   - Har bir qavat uchun shu jarayonni takrorlang.
   - So'nggi qavatni bezatib, rezavor mevalar bilan chiroyli ko'rinish bering.

5. Qotishi uchun:
   - Pirojniylarni xona haroratida 1 soat ushlab turing, keyin muzlatgichda 2 soat sovuting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_shaftolilimizq": """Shaftolili muzqaymoq🍧
    Masalliqlar:🍱
• Muzqaymoq uchun:
  o 250 gramm shaftolili pyure
  o 100 gramm shakar
  o 430 gramm suv
  o 5 gramm jelatin
  o 2 choy qoshiq limon sharbati
• Qiyomi uchun:
  o 250 gramm shakar
  o 110 gramm suv
  o 1/8 choy qoshiq limon kislotasi

Tayyorlash usuli:🍱
1. Qiyom tayyorlash:
   - Qozonchaga shakar va suvni soling, baland olovda shakar eriguniga qadar qaynatib turing.
   - Limon kislotasini ozroq suvda eritib, qiyomga qo‘shing.
   - Olovni pasaytirib, qiyom tillarangga kirguncha, taxminan 30-35 daqiqa davomida pishiring.

2. Muzqaymoq asosini tayyorlash:
   - Jelatinni 100 gramm suvda ivitib, bo‘kib chiqqandan so‘ng, gazda qizdiring (qaynab ketmasin).
   - Qolgan suvga shakar va tayyorlangan qiyomdan 60 grammini qo‘shing. Massani qaynatib, biroz sovuting.

3. Aralashmalarni birlashtirish:
   - Jelatinli aralashmani iliq qiyom bilan aralashtiring.
   - Shaftolili pyure va limon sharbatini qo‘shib, bir xil massa hosil bo‘lgunga qadar aralashtiring.

4. Tozalash va muzlatish:
   - Tayyor suyuqlikni doka ro‘mol yordamida tozalang.
   - Aralashmani qolipchalarga quyib, bir kechaga muzlatgichga qo‘ying.

5. Taqdim qilish:
   - Tayyor muzqaymoqni muzlatgichdan olib, yalpiz bargchalari va shaftoli bo‘laklari bilan bezating.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_aylanay": """Aylanay pirogi 🥧
    Masalliqlar:🍱
• Un – 400 g
• Soda – 0.5 choy qoshiq
• Xamirturush (qavartma) – 1.5 choy qoshiq
• Mayonez – 100 g
• Margarin – 200 g
• Murabbo (jem) – 0.5 litr

Tayyorlash usuli:🍱
1. Xamirni tayyorlash:
   - Margarinni qirg‘ichdan chiqarib, 2 stakan un bilan yaxshilab uvalang.
   - Hosil bo‘lgan aralashmadan yarim piyolani ajratib qo‘ying (keyin ustiga sepish uchun).

2. Xamirni aralashtirish:
   - Margarinli aralashmaga mayonez, tuxum va sodani qo‘shing.
   - Qolgan unni asta-sekinlik bilan qo‘shib, xamirga xamiryumshatgichni aralashtiring.
   - Yumshoq, bir xil xamir hosil bo‘lishi kerak.

3. Pirogni shakllantirish:
   - Tayyor xamirni gaz pechi patnisiga teng qilib yoying.
   - Ustiga murabbo (jem) surting.
   - Oldin ajratib qo‘yilgan margarinli unli aralashmani ustiga teng ravishda sepib chiqing.

4. Pishirish:
   - Gaz pechini 180 darajaga qizdiring.
   - Pirogni 30 daqiqa davomida oltin tusga kirguncha pishiring.

Tavsiyalar:
   - Murabboni xohlaganingizcha o‘zgartirishingiz mumkin (olxo‘ri, malina yoki o‘rik murabbosi juda mazali chiqadi).
   - Pirogni ustiga maydalangan yong‘oq yoki bodom sepib bezashingiz mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_chumoliuya": """Chumoli uyasi🥮
     Masalliqlar:🍱
• Tuxum – 2 dona
• Quyultirilgan sut – 0.5 litr
• Qatiq – 0.5 litr
• Margarin – 200 g
• Un – ta'bga ko‘ra

Tayyorlash usuli:🥮
1. Xamir tayyorlash:
   - Margarinni qirg‘ichdan chiqarib, un bilan aralashtiring.
   - Qatiqqa choy sodasi qo‘shib, margarinli un aralashmasiga soling.
   - Tuxumni qo‘shib, barcha masalliqlarni aralashtirib qattiq xamir qorib oling.
   - Tayyor bo‘lgan xamirni oziq-ovqat plyonkasiga o‘rab, 5-6 soatga muzlatgichga qo‘ying.

2. Pishirish:
   - Muzlatgichdan olingan xamirni qirg‘ichning yirik tishchasidan chiqarib oling.
   - Hosil bo‘lgan xamirni oldindan qizdirilgan gaz pechida oltin tusga kirguncha pishiring.
   - Pishgan xamirni sovuting.

3. Massani tayyorlash:
   - Sovigan xamirni mayda qilib maydalang.
   - Quyultirilgan sutni maydalangan xamirga qo‘shib, yaxshilab aralashtiring.

4. Shakl berish:
   - Tayyorlangan massaga qo‘l bilan uy shaklini bering yoki istalgan boshqa shakl yasang.
   - Istasangiz, yong‘oq, kokos zarralari, mayiz yoki boshqa qo‘shimchalar bilan bezating.

Tavsiyalar:🤗
   - Quyultirilgan sutning miqdorini xamirning yopishqoqligiga qarab sozlashingiz mumkin.
   - Shirinlikni muzlatgichda biroz tindirib, keyin tortiq qilsangiz, mazasi yanada yaxshiroq bo‘ladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_olchali": """Olchali pirog 🥧
     Masalliqlar:🍱
• Un – 2 stakan
• Shakar – 0.5 stakan
• Soda – 0.5 choy qoshiq
• Margarin – 170 g
• Olcha – 200 g
• Ko'knor urug'i – 1 osh qoshiq
• Tvorog – 300 g
• Tuxum – 2 dona
• Kakao (ixtiyoriy) – 1 osh qoshiq

Tayyorlash usuli:🍱
1. Xamir tayyorlash:
   - Blenderga margarin, shakar, kakao va unni solib, mayda kroshka hosil bo‘lguncha aralashtiring.
   - Tayyor kroshkani bir muddat muzlatgichga qo‘ying.

2. Nachinkani tayyorlash:
   - Tvorogga tuxum sarig‘ini va shakarni solib, blender yordamida yaxshilab aralashtiring.
   - Hosil bo‘lgan massaga un va ko‘knor urug‘ini qo‘shing.
   - Keyin olchani va alohida ko‘pirtirilgan tuxum oqini asta-sekin massaga aralashtiring.

3. Pirogni yig‘ish:
   - Pishirish qolipiga kroshkaning yarmini solib, tekis qilib joylashtiring.
   - Ustiga tvorogli nachinkani soling.
   - Eng yuqori qismiga qolgan kroshkani sepib, tekislang.

4. Pishirish:
   - Oldindan qizdirilgan gaz pechiga (180 °C) pirogni qo‘ying.
   - 40 daqiqa davomida o‘rta olovda, keyin yana 10 daqiqa davomida pastroq olovda pishiring.

5. Bezatish va tindirish:
   - Pirog biroz sovugandan so‘ng, eritilgan shokolad bilan ustini bezang (setka uslubida).
   - Tayyor pirogni muzlatgichga qo‘yib, kamida 2 soat tindiring.

Tavsiyalar:🤗
   - Pirogni sovugandan so‘ng iste’mol qilish mazaliroq bo‘ladi.
   - Olchaning suvi ko‘p bo‘lsa, uni oldindan biroz siqib olish kerak.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

})
# ---- KODNING DAVOMI (4-QISM, C) ----

recipes_texts.update({

    "dish_shokokeks": """Shokoladli keks🍪
     Masalliqlar:🍱
Kungaboqar yog‘i – 30 g
Un – 70 g
Shakar – 60 g
Tuxum – 1 dona
Tuz – 1 chimdim
Sut – 30 ml
Kakao kukuni – 15 g
Qavartma – 0.25 choy qoshiq

Tayyorlash usuli:🍱

1. Xamir tayyorlash:
   Barcha masalliqlarni (kungaboqar yog‘i, un, shakar, tuxum, tuz, sut, kakao va qavartma) bir idishda yaxshilab aralashtiring.
   Massaning bir xil konsistensiyaga ega bo‘lishiga ishonch hosil qiling.

2. Keksni shakllantirish:
   Tayyor xamirni bir chashkaga soling. Chashka yarmigacha to‘lishi kerak.

3. Pishirish:
   Chashkani mikroto‘lqinli pechga qo‘ying va eng yuqori haroratda 3,5 daqiqa davomida pishiring.
   Taxminan 2 daqiqadan keyin keks ko‘tarilishni boshlaydi. Bu tabiiy jarayon, xavotirlanmang.

4. Tayyorlash va xizmat qilish:
   Keks pishib chiqqach, mikroto‘lqinli pechdan chiqarib oling.
   Mikroto‘lqinli pechda tayyorlangan keks biroz quruqroq bo‘lishi mumkin, shuning uchun uni darhol issiqligida tanovul qilish tavsiya etiladi.

Maslahatlar:🤗
- Kekni muzqaymoq, shokolad sousi yoki yangi mevalar bilan bezash orqali yanada mazali qilish mumkin.
- Agar bir nechta porsiya kerak bo‘lsa, masalliqlar miqdorini mos ravishda oshiring.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "dish_asallipechenye": """Asalli pechenye🍩
     Masalliqlar:🍱
Un – 200 g
Shakar – 0,5 stakan
Tuxum – 2 dona
Asal – 2 osh qoshiq
Soda – 0,5 choy qoshiq
Margarin – 100 g

Tayyorlash usuli:🍱
1. Asalni tayyorlash:
   2 osh qoshiq asalni idishga solib, gaz plitasida qizdiring.
   Qaynab chiqqanidan so‘ng, 0,5 choy qoshiq soda qo‘shib, aralashtiring. Asal ko‘pira boshlaydi, darhol olovdan oling.

2. Margarin bilan aralashma tayyorlash:
   Xona haroratida yumshatilgan margarinni shakar va tuxum bilan yaxshilab aralashtiring.
   Sovigan asalni qo‘shing va yana yaxshilab aralashtiring.

3. Xamirni tayyorlash:
   Hosil bo‘lgan aralashmaga unni asta-sekin qo‘shib, qo‘lga yopishmaydigan yumshoq xamir qorib oling.

4. Xamirni yoyish va shakllar kesish:
   Ish stoli yoki taxtaga un sepib, xamirni taxminan 0,5 sm qalinlikda yoying.
   Maxsus qolipchalar yordamida turli shakllar kesib oling.

5. Pishirish:
   Pechenyelarni pergament qog‘oz yozilgan pishirish listiga tering.
   175 darajaga qizdirilgan duxovkada 15-20 daqiqa davomida pishiring.
   Pechenyelarning usti och jigarrang tusga kirganda, ularni duxovkadan oling.

6. Xizmat qilish:
   Pechenyelarni biroz sovitib, bolalaringiz va yaqinlaringiz bilan bahramand bo‘ling.

Maslahatlar:🤗
- Pechenyelarni qand-qaymoq bilan bezash mumkin.
- Shakar miqdorini ta’bga qarab kamaytirib yoki ko‘paytirishingiz mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
"""

})  # end of update
# ---- KODNING DAVOMI (4-QISM, D) ----

recipes_texts.update({

    # ICHIMLIKLAR BO‘LIMI:

    "drink_olmali": """Olmali choy 🍵
     Masalliqlar:🍱
Qora choy — 2-3 choy qoshiq
Olma — 40-50 gr
Shakar yoki asal — ta'bga ko‘ra

Tayyorlash usuli:🍱
1. Choynakni tayyorlang:
   Choynakni 3-4 marta qaynoq suv bilan chayib, issiqlikni saqlashga tayyorlang.

2. Choyni damlang:
   Choynakka qora choyni solib, darhol ustidan idishning 2/3 hajmicha qaynoq suv quying.
   Choyning turiga qarab 3 dan 15 daqiqagacha damlang.

3. Olma qo‘shish:
   Choyga mayda bo‘laklarga to‘g‘ralgan olmalarni qo‘shing.
   Ustidan yana qaynoq suv quying.

4. Damlanishi uchun qoldiring:
   Choynakni sochiq bilan yopib, 5 daqiqaga qoldiring.

5. Taqdim qilish:
   Tayyor bo‘lgan choyni piyolalarga suzib, ta'bga ko‘ra shakar yoki asal qo‘shing. Bu choyni issiq holda ichish qishki sovuq kunlarda iliqlik bag‘ishlaydi, yozda esa salqin holda ichish tetiklik beradi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_namatak": """Namatak sharbati 🧋
     Masalliqlar:🍱
1 piyola na’matak mevasi
2 litr suv

Tayyorlash usuli:🍱
1. Na’matakni tayyorlang:
   Na’matak mevasini yaxshilab tozalang va yuving.

2. Qaynatish:
   Na’matakni qopqog‘i zich yopiladigan idishga soling, ustidan 2 litr suv quying.
   Idishni o‘rtacha olovga qo‘yib, qaynatib chiqing. Keyin olovni pasaytirib, miltillatib 15 daqiqa davomida qaynatib pishiring.

3. Shirinlik qo‘shish:
   Agar shirinroq ichimlik istasangiz, qaynatish vaqtida ta’bga ko‘ra shakar qo‘shishingiz mumkin.

4. Damlanishi:
   Tayyor sharbatni o‘choqdan olib, idishning qopqog‘ini yopib, biroz damlab qo‘ying.

5. Sovutish yoki isitish:
   Sharbatni issiq holda sovuq kunlarda yoki salqin holda issiq kunlarda ichish mumkin.

Foydasi:🤗
Na’matak sharbati jigar, buyrak, ichak, oshqozon faoliyatini yaxshilaydi, qon aylanishini normallashtiradi va surunkali kasalliklarning oldini oladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.

""",

    "drink_yalpizlimon": """Yalpizli limon choy 🍸
     Masalliqlar:🍱
Shakar – 8-10 osh qoshiq
Suv – 2 litr
Yalpiz – 5-6 dona (barglari)
Limon – 1 dona
Choy (qora) – 3 choy qoshiq

Tayyorlash usuli:🍱
1. Suvni qaynatish:
   Idishga 2 litr suv quyib qaynatib oling.

2. Shakar qo‘shish:
   Suv qaynab chiqqach, unga shakar qo‘shib aralashtiring, shakar to‘liq erib ketishi kerak.

3. Choy va boshqa masalliqlarni qo‘shish:
   Gazni o‘chirib, idishga qora choy, parrak shaklda to‘g‘ralgan limon va yalpiz barglarini soling.

4. Damlash:
   Idishning ustini yopib, choyni 20 daqiqa damlashga qoldiring.

5. Tayyorlash:
   Tayyor choyni idishdan suzib olib, iliq yoki sovuq holda iching.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_qulupnay": """Qulupnayli ichimlik 🍹
    Masalliqlar:🍱
Qulupnay – 150 g
Shakar yoki asal – ta'bga ko'ra
Qatiq (kefir) – 300 ml
Yalpiz – 2 dona (bezak uchun)

Tayyorlash usuli:🍱
1. Qulupnayni tayyorlash:
   Qulupnayni yaxshilab yuvib, bandlaridan tozalang.

2. Qulupnayni ezish:
   Blender yordamida qulupnayni shakar yoki asal bilan birga ezib pyure holatiga keltiring. Blender bo'lmasa, qo'lda ezsangiz ham bo'ladi.

3. Qatiq qo'shish:
   Hosil bo'lgan qulupnay pyuresiga qatiq (kefir)ni soling va yana aralashtiring.

4. Ichimlikni bezash:
   Tayyor ichimlikni stakanlarga quying. Yalpiz yaproqlari bilan bezatib, darhol xizmat qiling.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_qovun": """Qovun sharbati 🍸
     Masalliqlar:🍱
Qovun – 600 g
Suv – 700 ml
Shakar – 200 g

Tayyorlash usuli:🍱
1. Qovunni tayyorlash:
   Qovunni po‘chog‘idan va urug‘laridan tozalang. Uni mayda bo‘laklarga kesing.

2. Shakar bilan aralashtirish:
   Qovun bo‘laklarini idishga soling, ustiga shakar seping va salqin joyda 2-3 soatga qoldiring. Bu vaqt davomida qovun shakar bilan aralashib o‘z sharbatini chiqaradi.

3. Qaynatish:
   Keyin idishga suv qo‘shing va aralashmani past olovda 5 daqiqa davomida qaynatib oling.

4. Sovutish:
   Tayyor sharbatni sovuting va muzlatkichda biroz saqlang.

5. Xizmat qilish:
   Sovuq holida stakanlarga quyib, taqdim eting. Istalgan holda yalpiz barglari bilan bezashingiz mumkin.

Foydasi:🤗
Qovun sharbati chanqoqni bosadi, suyak, tish va tirnoqlar uchun kaltsiy manbai bo‘lib xizmat qiladi, asab tizimini tinchlantiradi hamda organizmdagi suv va tuz muvozanatini saqlaydi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_bodomli": """Bodomli sut 🥛
     Masalliqlar:🍱
Asal – 2 osh qoshiq
Suv – 200 ml
Sut – 100 ml
Bodom – 30 dona

Tayyorlash usuli:🍱
1. Bodomni tayyorlash:
   Bodomni qaynoq suvga 5-10 daqiqaga solib qo‘ying.
   So‘ng mag‘izlarini po‘stlog‘idan tozalang.

2. Bodomni blenderda aralashtirish:
   Tozalangan bodomlarni blenderga soling, ustidan 200 ml suv quying.
   5 daqiqacha, orada to‘xtatib-to‘xtatib, blenderda ko‘pirtiring.

3. Sut va asal qo‘shish:
   Bodom aralashmasiga 100 ml sut va 2 osh qoshiq asal qo‘shing.
   Yana bir necha soniya davomida blenderda aralashtiring.

4. Sutni suzish (ixtiyoriy):
   Tayyor bo‘lgan aralashmani 4 qavatli dokadan suzib oling.
   Suzilgan bodomli sutni stakanga quying.

Qo‘shimcha ma’lumot:🤗
- Bodomli sutni suzmasdan ham ichishingiz mumkin.
- Agar sut yoqtirmasangiz, uni faqat suv bilan tayyorlab iste’mol qilsangiz ham bo‘ladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_uzum": """Uzum sharbati 🧋
     Masalliqlar:🍱
Uzum – 300 g
Shakar – 100 g
Suv – 1,5 l

Tayyorlash usuli:🍱
1. Tayyorlash:
   Uzumni yaxshilab yuvib, shoxchalaridan va barglaridan tozalang.

2. Qaynatish:
   Qaynab turgan suvga avval uzumni, keyin shakarni soling.
   10 daqiqa davomida qaynatib pishiring.

3. Sovutish:
   Tayyor sharbatni salqin holga keltirib, stakanga quyib xizmat qiling.

Foydali xususiyatlari:🤗
- Uzum sharbati chanqoqni yo‘qotadi, organizmga quvvat va tetiklik beradi.
- Yurak-qon tomir tizimiga ijobiy ta’sir ko‘rsatadi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_mevali": """Mevali sharbat 🍹
     Masalliqlar:🍱
3 litr suv
500 gramm o‘rik
300 gramm olcha yoki shpanka
200-220 gramm shakar

Tayyorlash usuli:🍱
1. Tayyorlash:
   O‘rik va olchani yaxshilab yuving.
   O‘rikni ikkiga bo‘lib, danagini olib tashlang.
   Olchani butunligicha qoldiring.

2. Qaynatish:
   Kastrulyaga suvni solib qaynatib oling.

3. Mevalarni qo‘shish:
   Qaynagan suvga o‘rik va olchani soling.
   O‘rtacha olovda 10 daqiqa davomida pishiring.

4. Shakar qo‘shish:
   Shakarni solib, yana 5 daqiqa davomida qaynatib oling.

5. Tindirish:
   Olovni o‘chiring, idishning qopqog‘ini yopib, 10-15 daqiqa tindirib qo‘ying.

6. Xizmat qilish:
   Sovitilgan kompotni stakanlarga quyib, dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_qatiq": """Qatiq 🍚
     Masalliqlar:🍱
Sut - 1 litr
Qatiq - 2-3 osh qoshiq
Yog‘liroq bo‘lishi uchun - 100-150 gramm qaymoq (ixtiyoriy)

Tayyorlash usuli:🍱
1. Sutni tayyorlash:
   Sutni yaxshilab qaynatib oling.
   Qaynatilgan sutni sirli idishga yoki issiqlikni yaxshi ushlab turadigan idishga quying.
   Sutni taxminan 5-10 daqiqa sovuting. Sut barmoqni kuydirmaydigan darajada iliq bo‘lishi kerak.

2. Qatiqni qo‘shish:
   Sutning ustida hosil bo‘lgan qaymoqli qoplamni imkon qadar buzmasdan, sutning o‘rtasidan qatiqni soling.
   Qatiqni aralashtirmasdan, shunchaki joylashtiring.

3. Dam olish:
   Idishning qopqog‘ini zich qilib yoping.
   Xona haroratida 8-10 soat davomida tindiring.

4. Muzlatgichga qo‘yish:
   Qatiqni tindirgach, muzlatgichga qo‘yib yana 2-3 soat sovuting. Bu qatiqning qalinlashishini ta’minlaydi va suvi chiqib ketmaydi.

5. Xizmat qilish:
   Tayyor qatiqni salatlarda, pishiriqlarda yoki shunchaki o‘zini ichish uchun foydalanishingiz mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_tarvuz": """Tarvuz sharbati🍹
     Masalliqlar:🍱
Tarvuz - 200 g
Shakar - 5 g (ixtiyoriy)

Tayyorlash usuli:🍱
1. Tarvuzni tayyorlash:
   Tarvuzni yaxshilab yuving va tozalang.
   Tarvuzni 4 qismga bo‘lib, po‘stlog‘idan ajratib oling.
   Qizil lahm qismini mayda bo‘laklarga bo‘ling.

2. Sharbat olish:
   Maydalangan tarvuz bo‘laklarini blenderda maydalang yoki qo‘lda siqib sharbati ajralguncha ishlov bering.
   Hosil bo‘lgan sharbatni mayda teshikli dokadan yoki elakdan suzib oling.

3. Shakar qo‘shish (ixtiyoriy):
   Agar sharbatga shirinlik qo‘shmoqchi bo‘lsangiz, ta'bga qarab shakar qo‘shing va yaxshilab aralashtiring.

4. Qaynatish (ixtiyoriy):
   Sharbatni tozalash va uzoq muddat saqlash uchun 5–10 daqiqa davomida qaynatib oling.

5. Sovutish va xizmat qilish:
   Sharbatni sovutib, sovuq holda xizmat qiling.

Foydalari:🤗
Tarvuz sharbati organizmdan suyuqlikni chiqarishga yordam beradi va jigar, buyrak xastaliklarida tavsiya etiladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_sabzi": """Sabzi sharbati 🥃
     Masalliqlar:🍱
Sabzi - 2-3 dona
Lavlagi suvi - 1 osh qoshiq

Tayyorlash usuli:🍱
1. Sabzini tayyorlash:
   Sabzining shirinroq va yangi turlarini tanlang.
   Sabzini yaxshilab yuving va po‘stini artib tozalang.

2. Sharbat siqish:
   Sabzini blender yoki sharbat chiqargich yordamida sharbatini siqib oling.
   Agar blenderda siqsangiz, keyin dokadan o‘tkazib, ortiqcha tolalarni olib tashlang.

3. Lavlagi suvi qo‘shish:
   Tayyor sabzi sharbatiga 1 osh qoshiq lavlagi suvi qo‘shing va yaxshilab aralashtiring.

4. Xizmat qilish:
   Sharbatni darhol ichish tavsiya etiladi, shunda foydali moddalar saqlanib qoladi.
   Agar xohlasangiz, bir necha bo‘lak muz qo‘shib, sovuq holda ichishingiz mumkin.

Foydalari:🤗
Sabzi sharbati immunitetni mustahkamlaydi, ko‘z nurini ravshanlashtiradi, ovqat hazm qilishni yaxshilaydi va buyrak faoliyatini qo‘llab-quvvatlaydi. Lavlagi suvi esa organizmni tozalashga yordam beradi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_zira": """Zira choy 🍵
     Masalliqlar:🍱
Qaynatilgan suv – 0,5 litr
Zira – 1 choy qoshiq
Choy (qora yoki yashil) – 1 choy qoshiq

Tayyorlash usuli:🍱
1. Choy tayyorlash:
   Choynakka zira va choyni soling.
   Ustidan 0,5 litr qaynagan suv quying.

2. Dam yedirish:
   Choynakning ustini yopib, 5-6 daqiqa dam yedirib qo‘ying.

3. Xizmat qilish:
   Tayyor zira choyini piyolalarga suzing va issiq holda iching.

Foydalari:🤗
Zira choyi nafaqat ishtahani ochadi va ovqat hazm qilishni yaxshilaydi, balki organizmni yengillashtiradi va immunitetni mustahkamlaydi. Ibn Sino ta’kidlaganidek, zira organizmni tozalashda, nafas olishni yengillashtirishda va oshqozonning turli muammolarida foydali.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_vitaminli": """Vitaminli ichimlik🍵
    Masalliqlar:🍱
Asal – 1 choy qoshiq
Sarimsoqpiyoz donasi – 1 dona
Na'matak – 1 osh qoshiq
Qaynatilgan suv – 250 ml
Limon – 25 gr
Zanjabil – 20 gr

Tayyorlash usuli:🍱
1. Zanjabilni tayyorlash:
   Zanjabil ildizining 2 sm qismini tozalang va yupqa qilib kesib oling.

2. Sarimsoqni maydalash:
   Sarimsoq donasini po‘stidan tozalab, mayda to‘g‘rang.

3. Masalliqlarni aralashtirish:
   Quritilgan na'matakni yuvib, zanjabil va sarimsoq bilan birga termosga soling.

4. Dam yedirish:
   Ustidan qaynab turgan suvni quying va termosning qopqog‘ini yoping.
   Ichimlikni 2 soat davomida damlashga qo‘ying.

5. Tayyorlashni yakunlash:
   Damlangan ichimlikni tindirib, unga asal va limon qo‘shib yaxshilab aralashtiring.

Foydalari:🤗
Bu ichimlik organizmni isintiradi, immunitetni mustahkamlaydi va ishtahani pasaytirishga yordam beradi. Sarimsoqning ta’mi ichimlikda deyarli bilinmaydi, ammo uning foydasi kuchli.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drink_moxito": """Moxito🍹
    Masalliqlar:🍱
Yangi uzilgan yalpiz – 10 g
Laym yoki limon – yarimta
Sprayt – 150 ml
Muz – 8 bo‘lak
Shakar – 1 choy qoshiq

Tayyorlash usuli:🍱
1. Laym tayyorlash:
   Laym yoki limonni ikkiga bo‘ling va bokalga soling.

2. Yalpiz va shakar qo‘shish:
   Laym bo‘laklariga yangi yalpiz va shakar qo‘shing. Ularni ezib, birgalikda yaxshilab aralashtiring.

3. Muz qo‘shish:
   Aralashmaga muz qirindisi yoki bo‘laklarini soling.

4. Aralashmani urish:
   Sheyker yordamida aralashmani yaxshilab urib bir xil bo‘lishiga erishing.

5. Sprayt quyish:
   Tayyorlangan aralashmani bokalga soling va ustidan sprayt quyib, aralashtiring.

6. Bezash:
   Kokteylni laym bo‘lagi va yalpiz yaproqchalari bilan bezating.

Maslahat:🤗
Sprayt mavjud bo‘lmasa, shakarli sirop va gazlangan mineral suvdan foydalanishingiz mumkin. Shakarli siropni tayyorlash uchun qaynoq suvga shakarni to‘liq eriguncha aralashtirib qo‘shing va sovuting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    # TORTLAR BO‘LIMI:

    "tort_praga": """Praga torti 🍰
     Masalliqlar:🍱
Biskvit uchun:
Un – 115 gr
Shakar – 150 gr
Tuxum – 6 dona
Kakao kukuni – 25 gr
Margarin – 40 gr

Krem uchun:
Sut – 1,5 piyola
Shakar – 200 gr
Un – 3 osh qoshiq
Saryog‘ – 250 gr

Shokoladli massa uchun:
Shokolad – 50 gr
Saryog‘ – 50 gr

Tayyorlash usuli:🍱

Biskvit tayyorlash:
1. Tuxum oqini sarig‘idan ajrating.
2. Tuxum oqiga 75 gr shakar qo‘shib, 2-3 daqiqa mikserda ko‘pirtiring.
3. Tuxum sarig‘ini qolgan 75 gr shakar bilan mikserda alohida ko‘pirtirib, eritilgan margarin qo‘shib aralashtiring.
4. Un va kakaoni aralashtirib, tuxum sarig‘i massasiga qo‘shing.
5. Tuxum oqi ko‘pirtirilgan massani asta-sekinlik bilan tuxum sarig‘iga solib, yumshoq harakatlar bilan aralashtiring.
6. Tayyor xamirni yog‘langan qolipga quying va 200°C haroratda 30 daqiqa davomida pishiring.

Krem tayyorlash:
1. Un va shakarni bir idishda aralashtiring, so‘ng sut qo‘shing va yaxshilab aralashtiring.
2. Past olovda, doimiy aralashtirib turib, massani quyuqlashguncha qizdiring. Sovuting.
3. Saryog‘ni mikserda 2 daqiqa ko‘pirtiring. Sovigan sutli massani asta-sekin qo‘shib, mikser yordamida bir xil krem hosil bo‘lgunga qadar aralashtiring.

Shokoladli massa tayyorlash:
1. Saryog‘ va shokoladni suvli vannada eritib, aralashtiring.

Tortni yig‘ish:
1. Sovigan biskvitni 3 qismga ajrating.
2. Har bir qatlamga krem surtib, tortni yig‘ing.
3. Ustini va yon qismlarini ham krem bilan qoplang.
4. Shokoladli massani tort yuziga chiziqchalar shaklida chizib, bezating.

Muzlatish:❄️
Tayyor tortni muzlatgichda kamida 2 soat saqlang, so‘ng dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_napaleon": """Napaleon torti 🥮
     Masalliqlar:🍱
2 o‘ram tayyor «MUZA» qatlamli xamiri
400 gr quyultirilgan sut (1 banka)
180-200 gr yumshatilgan saryog‘ (82,5% yog‘lilik)
250 ml yog‘liligi 33% bo‘lgan qaymoq

Tayyorlash usuli:🍱
1. Korjlarni tayyorlash:
   1) Qatlamli xamirni xona haroratida eritib oling.
   2) Xamirni 3-4 bo‘lakka bo‘ling va har bir bo‘lakni yupqa qilib, taxminan 24-26 sm diametrda yoying.
   3) Yoyilgan xamirni likopcha yordamida kesib, chetlarini tekislang.
   4) Xamirni sanchqi yordamida ko‘proq teshib chiqing, shunda u pishayotganda shishib ketmaydi.
   5) Duxovka tovasiga pergament qog‘ozini solib, 200°C darajada 15 daqiqa davomida korjlarni tillarang tusga kirguncha pishiring.
   6) Qolgan xamir bo‘laklarini ham pishirib, maydalab, ustiga sepish uchun tayyorlang.

2. Krem tayyorlash:
   1) Quyultirilgan sut va yumshatilgan saryog‘ni mikser yordamida past tezlikda yaxshilab aralashtiring.
   2) Alohida idishda sovutilgan qaymoqni ko‘pirtiring, shunda u qattiq va momiq massa hosil qiladi.
   3) Ko‘pirtirilgan qaymoqni quyultirilgan sutli aralashmaga qo‘shib, bir xil massa hosil bo‘lguncha aralashtiring.

3. Tortni yig‘ish:
   1) Har bir korjga krem surting va bir-birining ustiga qo‘ying.
   2) Tortning ustki va yon qismlariga ham krem surtib, bir xil qilib tekislang.
   3) Maydalangan xamir bo‘laklarini tortning ustki qismiga va yon tomonlariga seping.

4. Sovutish:
   Tortni kamida 6-8 soat davomida muzlatgichda tindiring. Shu vaqt ichida krem korjlarga yaxshi singadi va tort yanada mazali bo‘ladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "drezden_drezden": """Drezdencha tort 🧁
     Masalliqlar:🍱
Xamiri uchun:
150 gramm un
70 gramm shakar
1 dona tuxum
50 gramm sariyog'
1/2 choy qoshiq qabartma

1-qavat asosi:
500 gramm tvorog
150 gramm shakar
2 ta tuxum
1 osh qoshiq quruq vanilli puding

2-qavat asosi:
1 o‘ramcha quruq vanilli puding
500 millilitr sut
100 gramm sariyog'
3 ta tuxum sarig'i
3 ta tuxum oqi
3 osh qoshiq shakar

Tayyorlash usuli:🍱

Xamiri:
1. Tuxum va shakarni yaxshilab ko'pirtiring.
2. Yumshatilgan sariyog'ni qo'shib, bir xil massa hosil bo'lguncha aralashtiring.
3. Elangan un va qabartmani qo'shib, xamir qorib oling.
4. Xamirni 30 daqiqaga muzlatgichga olib qo'ying.

1-qavat asosi (tvorogli qatlam):
1. Tvorogni idishga solib, shakar va tuxumlarni qo'shing.
2. Mikser yordamida silliq massa hosil bo'lguncha ko'pirtiring.
3. 1 osh qoshiq quruq puding qo'shib, yaxshilab aralashtiring.

2-qavat asosi (pudingli qatlam):
1. Puding kukunini sut bilan aralashtirib, gazga qo'ying va muntazam aralashtirib, quyulguncha pishiring.
2. Pishgan pudingni sovutib, sariyog' va tuxum sarig'larini qo'shing.
3. Alohida idishda tuxum oqini shakar bilan ko'pirtirib, yumshoq ko'pik holatiga keltiring.
4. Ko'pirtirilgan tuxum oqini pudingli massaga ehtiyotkorlik bilan qo'shing.

Tortni yig'ish:
1. Xamirni qolipga joylashtirib, tekis qilib yoying.
2. Xamir ustiga tvorogli asosni quying.
3. Tvorogli asos ustiga pudingli qatlamni quying.

Pishirish:
1. Tortni 180 °C darajada qizdirilgan gaz pechiga qo'ying.
2. 60 daqiqa davomida pishiring. Tort pishayotganda pechni ochmang, bu uning ustini yorilishiga sabab bo'lishi mumkin.
3. Pishgan tortni pechda 15-20 daqiqa qoldiring, so'ngra sovutib, bir kecha davomida muzlatgichga qo'ying.

Bezatish:🤗
Tortni ustini xohlagan mevalar yoki meva bo‘lakchalari bilan bezating.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_zebra": """Zebra torti 🍥
     Masalliqlar:🍱
Un — 2 stakan
Shakar — 1 stakan
Tuxum — 2 dona
Soda — 1 choy qoshiq
Qatiq — 1 stakan
Kakao kukuni — 1 osh qoshiq
Margarin — 200 gr

Tayyorlash usuli:🍱
1. Qatiqni tayyorlash:
   Qatiqqa soda solib, ko'piklanguncha aralashtiring.

2. Xamirni tayyorlash:
   Boshqa idishda tuxum va shakarning ko'pirtirilgan massasini tayyorlang.
   Eritilgan margarin, un va qatiqni qo'shib, bo'tqasimon xamir hosil qiling.

3. Xamirni ajratish:
   Xamirni teng ikkiga ajrating.
   Bir qismiga kakao kukuni qo'shib yaxshilab aralashtiring.

4. Qolipga quyish:
   Qolipni yog'lang.
   Xamirning oq qismidan 1 osh qoshiq, so'ngra kakaoli qismidan 1 osh qoshiq ustma-ust joylashtiring. Shu tartibda davom ettiring.

5. Pishirish:
   Qolipni 180 darajagacha qizdirilgan pechga qo'ying.
   Tortni 30 daqiqada pishiring. Tayyorligini tish cho'pi bilan tekshiring.

Shokoladli glazur tayyorlash:
1. Masalliqlarni aralashtirish:
   Shakar, kakao, sutni bir idishga solib yaxshilab aralashtiring.
   Suv bug'ida aralashmaga sariyog' qo'shib, 5-6 daqiqa davomida aralashtirib turing.

2. Tort yuzasiga quyish:
   Tayyor glazurni issiqligida tortning yuziga surtib chiqib, kokos bo'lakchalari yoki boshqa bezaklar bilan bezang.

Tayyor!🤗
Mazali "Zebra" tortingizni dasturxonga torting!
Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_pancho": """Pancho torti 🥮
     Masalliqlar:🍱
Xamiriga:
Tuxum — 6 dona
Un — 200 g
Kakao kukuni — 4 osh qoshiq
Shakar — 250 g
Qabartma — 1 choy qoshiq

Kremiga:
Yog'li smetana (25% va undan yuqori) — 400 g
Yog'li qaymoq — 200 g
Shakar — 150 g
Vanil shakari — 1 choy qoshiq

Asosiga:
Konservalangan ananas halqachalari — 4-5 dona
Tozalangan yong'oq — 1 stakan

Ustiga:
Qora shokolad — 50 g
Sariyog' — 30 g

Tayyorlash usuli:🍱
Xamir tayyorlash:
1. Gaz pechini 170 °C darajaga oldindan qizdiring. Tort qolipini pergament qog‘ozi bilan to‘shang.
2. Tuxumlarni mikserda 5 daqiqa davomida ko'pirtiring, shakarni asta-sekin solib, yanada ko'pirtiring.
3. Alohida idishda un, qabartma va kakaoni elab, tuxumli aralashmaga oz-ozdan qo‘shing, pastdan tepaga ehtiyotkorlik bilan aralashtiring.
4. Xamirni qolipga quying, 170 °C da 35-40 daqiqa davomida pishiring. Biskvit tayyor bo'lgach, sovuting va pelyonkaga o‘rab, 1 kechaga qoldiring.

Krem tayyorlash:
1. Smetana va shakarni aralashtiring.
2. Sovuq qaymoqni mikserda ko‘pirtirib, smetanali massaga qo‘shing.
3. Vanil shakari solib, yana biroz aralashtiring.

Tortni yig‘ish:
1. Sovigan biskvitni bir qalin va bir yupqa qatlamga bo‘ling.
2. Yupqa qatlamni likopchaga joylashtirib, ustiga ananas suvidan 7-8 qoshiq quyib namlantiring.
3. Krem surtib, ustidan maydalangan yong'oq va to'g'ralgan ananas seping.
4. Qalin biskvitni 2-3 sm bo‘laklarga kesib, kremga botiring va tepaliksimon ko‘rinishda joylashtiring.
5. Tort ustiga ham krem surting, silliqlang.

Glazur tayyorlash:
1. Shokolad va sariyog'ni suv bug'ida eritib, aralashtiring.
2. Biroz sovigach, qopchaga soling va tort ustiga chiziqlar shaklida bezang.
3. Yong'oq bilan ham bezashingiz mumkin.

Tugallash:🤗
1. Tortni kamida 3 soatga muzlatgichda tindiring.
2. Choy yoki qahva bilan dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_medovik": """Medovik torti 🥮
     Masalliqlar:🍱
Xamiri uchun:
Un — 4 stakan
Shakar — 1 stakan
Sariyog' — 150 g
Tuxum — 3 dona
Asal — 2 osh qoshiq
Soda — 1 choy qoshiq

Krem uchun:
Sut — 1 piyola
Shakar — 1 piyola
Un — 3 osh qoshiq
Kakao — 1 choy qoshiq
Sariyog' — 50 g

Tayyorlash usuli:🍱
Xamirni tayyorlash:
1. Gaz ustida asalni eritib, ustiga 0,5 choy qoshiq soda qo‘shing. Massani qizargunicha aralashtiring.
2. Asalli aralashmaga sariyog' qo‘shib, eriguncha aralashtiring va olovdan oling.
3. Boshqa idishda tuxumni shakar bilan birga aralashtiring.
4. Tuxumli aralashmaga asalli massa va unni oz-ozdan qo‘shib, yumshoq xamir qorib oling.
5. Xamirni 4 bo'lakka bo‘lib, zuvalachalar hosil qiling.

Korjlarni tayyorlash:
1. Har bir zuvalani yupqa qilib yoying.
2. Yog'langan gaz listiga qo'yib, 180 °C darajali pechda 10-15 daqiqa davomida pishiring.
3. Pishgan korjlarning chetlarini issiqligida kesib, bo'laklarini maydalab, ustiga sepish uchun chetga olib qo'ying.

Kremni tayyorlash:
1. Sut, shakar, un va kakaoni birga aralashtiring.
2. Gaz ustiga qo'yib, doimiy aralashtirib, quyuqlashguncha qaynatib oling (2-3 daqiqa).
3. Massaga sariyog'ni qo‘shib, eriguncha aralashtiring.

Tortni yig'ish:
1. Har bir korjning ustiga issiq kremdan surting.
2. Korjlarni bir-birining ustiga qo'yib, oxirgi qavatni ham krem bilan surting.
3. Tortning ustiga maydalangan korj bo‘laklarini sepib, selofan bilan yopib qo‘ying.
4. Tortni kamida 4-5 soat, yaxshisi, bir kechaga tindiring.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_frezye": """Frezye torti 🍰
    Masalliqlar:🍱
Biskvitli korj uchun:
Tuxum — 3 dona
Shakar — 100 g
Un — 50 g
Makkajo‘xori kraxmali — 25 g
Qabartma — 1 choy qoshiq
Vanil shakari — 10 g

Kremli asos uchun:
Sut — 400 ml
Shakar — 200 g
Tuxum — 3 dona
Makkajo‘xori kraxmali — 60 g
Sariyog‘ — 200 g
Jelatin — 15 g
Sovuq suv — 50 ml
Vanil shakari — 10 g
Qulupnay — 800 g

Tayyorlash usuli:🍱
Korj tayyorlash:
1. Tuxum oqini sarig‘idan ajratib, oqini ko‘pirtiring. Ko‘pirtirish jarayonida shakarni asta-sekin qo‘shing.
2. Tuxum sarig‘ini alohida idishda shakar va vanil shakari bilan ko‘pirtiring.
3. Elangan un, kraxmal va qabartmani aralashtirib, tuxum sarig‘iga soling.
4. Tuxum oqi ko‘pirtirilgan massani ehtiyotkorlik bilan qo‘shib, pastdan tepaga aralashtiring.
5. Xamirni pergament qog‘oziga diametri 22 sm bo‘lgan doira shaklida yoyib, 190 °C darajali pechda 12-14 daqiqa pishiring.
6. Xamirning qolgan qismidan xuddi shunday ikkinchi korj pishirib, sovuting.

Krem tayyorlash:
1. Sut va shakarni yarmisini olovga qo‘yib, qaynatib oling.
2. Boshqa idishda tuxum, kraxmal, qolgan shakar va vanil shakari aralashtiring.
3. Qaynoq sutni tuxumli aralashmaga sekin-asta quying, doimiy ravishda aralashtirib turing.
4. Aralashmani past olovga qo‘yib, quyuq krem holatiga kelguncha aralashtiring.
5. Sovigan kremga yumshagan sariyog‘ning yarmini qo‘shib, mikserda ko‘pirtiring.
6. Jelatinni suvga solib 15 daqiqa tindiring. Isitib, kremga qo‘shing va yaxshilab aralashtiring.

Tortni yig‘ish:
1. Sovigan korjni likopchaga qo‘ying va atrofiga olinadigan qolip chetini o‘rnating.
2. Qulupnaylarni bo‘lib, kesilgan joyi qolipga qaragan holda korj atrofiga terib chiqing.
3. Kremning uchdan bir qismini korj ustiga quyib, qolgan qulupnaylarni butun holda terib chiqing.
4. Qolgan kremni ustiga quyib, ikkinchi korjni qo‘ying va yana krem surting.
5. Tortni yopishqoq plyonka bilan yopib, muzlatgichga 8-10 soatga qo‘ying.
6. Sovigan tortni qulupnay bilan bezatib, dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_karamel": """Karamel va yong’oqli tort🎂
     Masalliqlar:🍱
Xamiri uchun:
Un — 250 g
Yumshatilgan sariyog‘ — 150 g
Shakar — 80 g
Tozalangan yeryong‘oq — 130 g
Tuxum — 1 dona
Qabartma — 1 choy qoshiq

Kremi uchun:
Qaynatilgan quyultirilgan sut — 300 g
Smetana — 300 g

Ustiga sepish uchun: Tozalangan yeryong‘oq

Tayyorlash usuli:🍱
1. Xamirni tayyorlash:
   - Yumshatilgan sariyog‘ va shakarni idishga solib, mikserda 2-3 daqiqa ko‘pirtiring. Massa oqarib, bir tekis bo‘lishi kerak.
   - Tuxumni qo‘shib, yana 2 daqiqa davomida ko‘pirtiring.
   - Tozalangan yeryong‘oqni quruq tovada 5-7 daqiqa qovurib, sovuting va blenderda maydalang.
   - Yeryong‘oq uvog‘ini sariyog‘li aralashmaga qo‘shib, lopata bilan aralashtiring.
   - Un va qabartmani aralashtirib, sariyog‘li massaga elab soling. Dastlab lopata yordamida aralashtirib, keyin qo‘l bilan yumshoq xamir qoring.
   - Tayyor xamirni plyonkaga o‘rab, muzlatgichda 30 daqiqa dam oling.

2. Kremni tayyorlash:
   - Qaynatilgan quyultirilgan sutni smetana bilan mikserda yaxshilab aralashtiring.
   - Tayyor kremni yopishqoq plyonka bilan yoping va muzlatgichga qo‘yib, tindiring.

3. Korjlarni tayyorlash:
   - Sovigan xamirni 6 ta bo‘lakka bo‘ling (har biri taxminan 100 g).
   - Har bir bo‘lakni 0,3 sm qalinlikda yoyib, 22 sm diametrli dumaloq shaklga keltiring.
   - 190 °C darajali pechda har bir korjni 7 daqiqa davomida tillarang tusga kirguncha pishiring.
   - Pishgan korjlarni sovutib oling.

4. Tortni yig‘ish:
   - Dumaloq olinadigan qolipni foydalanib, korjlarni ketma-ketlikda krem bilan surting. Oxirgi korj ustiga krem surtmasdan qoldiring.
   - Tortni yopishqoq plyonka bilan o‘rab, 2-3 soat davomida tindiring.

5. Bezatish:
   - Tortning ustki va yon tomonlariga krem surting.
   - Ta’bga ko‘ra maydalangan yeryong‘oq bilan ustini va yonlarini bezang.
   - Tortni sovutib, dasturxonga torting.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_kitakat": """Kita-kat torti🍰
     Masalliqlar:🍱
Biskviti uchun:
Tuxum – 4 dona
Shakar – 150 g
Un – 165 g
Vanilin – 0.5 choy qoshiq
Sut – 120 ml
Sariyog‘ – 60 g
Qabartma – 1 choy qoshiq
Tuz – bir chimdim

Shimdirish uchun:
Shirin qiyom – 50 ml

Kremi uchun:
Tvorogli pishloq – 400 g
35% yog‘li qaymoq – 300 g
Shakar upasi – 200 g
Malina – 150 g

Bezatish uchun:
Kit-kat shokoladli plitkasi – 10 dona
Har xil rezavor mevalar yoki yong‘oqlar

Tayyorlash usuli:🍱
1. Biskvit tayyorlash:
   1) Gaz pechini 170°C darajaga oldindan qizdiring. Tort qolipini pergament qog‘ozi bilan to‘shang.
   2) Tuxumlarni idishga chaqib, bir chimdim tuz soling va ozroq ko‘pirtiring.
   3) Shakar va vanilin qo‘shib, mikserda 5 daqiqa davomida massa ikki baravar ko‘payguncha ko‘pirtiring.
   4) Un va qabartmani elab, tuxumli aralashmaga 3 qismda qo‘shing va ehtiyotkorlik bilan lopatka yordamida aralashtiring.
   5) Sut va sariyog‘ni qizdirib (qaynatmasdan), xamirga qo‘shing va yaxshilab aralashtiring.
   6) Tayyor xamirni qolipga quying va 170°C da 35-40 daqiqa davomida pishiring.
   7) Biskvitni qolipdan chiqarib, pelyonkaga o‘rab, sovutgichda 1 kechaga qoldiring.

2. Krem tayyorlash:
   1) Tvorogli pishloq va shakar upasini mikser yordamida ko‘pirtiring.
   2) Muzdek qaymoqni qo‘shib, yana bir necha daqiqa ko‘pirtiring.
   3) Kremni ikki qismga bo‘ling. Ko‘proq qismiga malina qo‘shib, aralashtiring. Kichik qismini tortni bezatish uchun saqlang.

3. Tortni yig‘ish:
   1) Sovigan biskvitni uch qismga bo‘ling.
   2) Birinchi korj ustiga qiyom surtib, malinali kremning yarmini surting.
   3) Ikkinchi korjni qo‘shib, qolgan malinali kremni surting va uchinchi korj bilan yopib qo‘ying.
   4) Qolgan kremni tortning ustki va yon tomonlariga surting.

4. Tortni bezatish:
   1) Tort chetlarini Kit-kat shokoladlari bilan bezang va ularni lenta bilan bog‘lang.
   2) Tort ustiga rezavor mevalar yoki yong‘oqlar bilan bezak bering.
   3) Tortni 2-3 soatga sovutgichga qo‘yib, tindiring.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_boston": """Bostoncha kremli tort 🥮
     Masalliqlar:🍱
Kremi uchun:
Sut – 500 ml
Tuxum – 2 dona
Shakar – 100 g
Makkajo'xori kraxmali – 30 g
Sariyog‘ – 50 g

Biskviti uchun:
Un – 125 g
Qabartma – 1 choy qoshiq
Shakar – 150 g
Tuxum – 4 dona
O‘simlik yog‘i – 3 osh qoshiq

Glazuri uchun:
Qora shokolad – 150 g
Qaymoq – 50 ml

Tayyorlash usuli:🍱
1. Biskvit tayyorlash:
   1) Tuxum oqini sarig‘idan ajratib oling.
   2) Tuxum oqini shakar bilan qattiq holga kelguncha mikser yordamida ko‘pirtiring.
   3) Tuxum sarig‘ini o‘simlik yog‘i bilan aralashtiring va oq aralashmaga qo‘shing.
   4) Un va qabartmani elab, aralashmaga soling va ehtiyotkorlik bilan aralashtiring.
   5) Xamirni tort qolipiga solib, 175°C da 30–35 daqiqa davomida pishiring.

2. Krem tayyorlash:
   1) Sutni qaynating.
   2) Tuxum, shakar va kraxmalni alohida idishda aralashtiring.
   3) Qaynagan sutni tuxumli aralashmaga asta-sekinlik bilan quyib, aralashtiring.
   4) Aralashmani qozonga qaytaring va o‘rtacha olovda quyulguncha pishiring.
   5) Krem sovigach, sariyog‘ni qo‘shing va yaxshilab aralashtiring.

3. Tortni yig‘ish:
   1) Sovigan biskvitni ikki qismga bo‘ling.
   2) Birinchi qatlamga kremning yarmidan surting.
   3) Ikkinchi biskvitni ustiga qo‘yib, qolgan krem bilan tortni ustini va yonlarini qoplang.

4. Glazur tayyorlash:
   1) Qora shokoladni qaymoq bilan birga suv bug‘ida eritib, yaxshilab aralashtiring.
   2) Glazurni tort ustiga quying va teng taqsimlang.

5. Sovutish va bezatish:
   1) Tayyor tortni 2–3 soatga muzlatgichda tindiring.
   2) Xohishingizga ko‘ra, ustini rezavor mevalar yoki yong‘oqlar bilan bezating.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_bounty": """Bounty torti 🍥
     Masalliqlar:🍱
Korj uchun:
Un – 95 g
Tuz – bir chimdim
Kakao – 1 osh qoshiq
Vanil shakari – 1 choy qoshiq
Tuxum – 3 dona
Shakar – 200 g
Tez eriydigan qahva – 1 choy qoshiq
Sariyog‘ – 170 g
Qora shokolad – 90 g

Asos uchun:
Kokos qirindisi – 150 g
Quyultirilgan sut – 340 g

Ganash uchun:
Yog‘li qaymoq (35%) – 120 ml
Qora shokolad – 180 g
Sariyog‘ – 50 g

Tayyorlash tartibi:🍱
1. Korj tayyorlash:
   1) Tog‘orachaga sariyog‘ va shokoladni soling, suv bug‘ida aralashtirib eritib oling.
   2) Eritilgan aralashmaga shakar va qahvani solib, venchik yordamida aralashtiring.
   3) Tuxumlarni bittadan qo‘shib, yaxshilab aralashtiring.
   4) Vanil shakari, tuz, kakao va unni aralashmaga solib, bir xil massa hosil bo‘lgunga qadar aralashtiring.
   5) 22-24 sm lik qolipni yog‘lab, tagiga pergament qog‘oz to‘shang. Xamirni quyib, 175°C haroratda 25-30 daqiqa davomida pishiring.
   6) Pishgan korjni sovigunicha qolipda qoldiring.

2. Asos tayyorlash:
   1) Quyultirilgan sut va kokos qirindisini aralashtiring.
   2) Sovigan korj ustiga kokosli asosni solib, tekislang.

3. Ganash tayyorlash:
   1) Qaymoqni qozonchaga solib, qaynatmasdan qizdiring.
   2) Issiq qaymoqqa bo‘laklarga bo‘lingan shokoladni qo‘shing va aralashtiring.
   3) Shokolad to‘liq erigach, sariyog‘ni qo‘shib, silliq massa hosil bo‘lgunga qadar aralashtiring.

4. Tortni yig‘ish:
   1) Tayyor ganashni tort ustiga quying va tekislang.
   2) Tortni kamida 1 soatga, yaxshisi bir kechaga sovutgichda qoldiring.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "tort_pavlova": """Pavlova torti 🍰
     Masalliqlar:🍱
Merenga uchun:
Tuxum oqi – 150 g
Shakar upasi – 200 g
Shakar – 100 g
Istalgan rezavor mevalar

Krem uchun:
Yog'li qaymoq (35%) – 250 g
Quyultirilgan sut – 150 g
Istalgan rezavor mevalar

Tayyorlash usuli:🍱
1. Merenga tayyorlash:
   1) Tuxum oqini mikserda shakar upasini oz-ozdan qo‘shib, asta-sekin ko‘pirtiring.
   2) Tuxum oqi yetarlicha qalinlashib, barqaror holga kelgach, shakarni oz-ozdan qo‘shing va qattiq cho‘qqilar hosil bo‘lgunga qadar ko‘pirtiring.
   3) Pergament qog‘oziga 20-22 sm diametrda doira chizib, merengani doira ichiga joylashtiring. Yon qismlari markazdan biroz balandroq bo‘lishi kerak, markazida chuqurcha hosil qiling.
   4) 150°C darajada qizdirilgan gaz pechida 1 soat 30 daqiqa davomida pishiring. Pishgan merengani pechdan olib, sovushini kuting.

2. Krem tayyorlash:
   1) Sovuq qaymoqni mikser yordamida, o‘rtacha tezlikda, barqaror holatga kelgunicha ko‘pirtiring.
   2) Quyultirilgan sutni oz-ozdan qo‘shib, qaymoqni qattiq pik holatiga kelguncha ko‘pirtirishda davom eting.

3. Tortni yig‘ish:
   1) Sovigan merenganing markazidagi chuqurchaga kremni ehtiyotkorlik bilan joylashtiring.
   2) Ustiga rezavor mevalar bilan bezang. Mevalarni xohishingizga ko‘ra tanlang.

Yoqimli ishtaha!🍽️😋 
Yordam bera olgan boʻlsam hursandman.
""",

    # NONLAR BO‘LIMI:

    "non_qatlamapatir": """Qatlama patir 🫓
     Masalliqlar:🍱
Un: 1 kg
Suv: 500 ml
Tuz: 30 gr (bir osh qoshiq)
Margarin: 300 gr
Xamirturush: 10-15 gr

Tayyorlash usuli:🍱

1. Xamirni tayyorlash:
   1) Xamirni qorish:
      Un, suv va tuzni birlashtirib, qattiqroq, yoyishga yaroqli xamir qoriladi. Xamirni tindiring, ammo oshib ketmasin. Oshgan xamir qatlamlar hosil qilishda yaroqsiz bo‘lib qolishi mumkin.
   2) Margarinni tayyorlash:
      Margarinni yumshoq va yopishqoq holatda bo‘lishi kerak. Sutli margarin tanlash tavsiya etiladi. Margarinni biroz ezib, plastilin kabi yopishqoq ekanligiga ishonch hosil qiling.

2. Xamirni yoyish va qatlamlash:
   1) Xamirni yoyish:
      Tindirilgan xamirni juvada katta doira shaklida yoying.
   2) Margarin surish:
      Yumshatilgan margarin xamirning yarmiga qo‘l bilan bir tekis suriladi.
   3) Xamirni qatlash:
      - Margarinsiz yarmi bilan ustini yoping.
      - Past qismini yuqoriga qayiring, ikkita qatlam hosil bo‘ladi.
      - Yon taraflarini o‘rtaga taxlang va oxirida chap qismini o‘ng tomonga buklang.
   4) Muzlatgichga qo‘yish:
      Xamirni paketga solib, 20-30 daqiqaga muzlatgichda tindiring.

3. Qatlamlashni takrorlash:
   - Muzlatgichdan olgan xamirni yana yoying va avvalgi bosqichlarni takrorlang.
   - Buni jami 3 marta amalga oshiring.

4. Xamirni shakllantirish:
   1) Tasmalarga kesish:
      Yoyilgan xamirni uzun-uzun tasmalarga kesing.
   2) O‘rash:
      Har bir tasmani o‘rab, uchini pastiga bostirib qo‘ying.

5. Pishirish:
   1) Yoyish:
      Har bir o‘ralgan xamirni juvada yoying va o‘rtasiga chekich bilan chizik hosil qiling.
   2) Tuxum surish:
      Ustiga tuxum surtib, chiroyli ko‘rinish berish uchun tayyorlang.
   3) Pishirish:
      Dimxonada (200°C haroratda) 20-30 daqiqa davomida tillarang tusga kirguncha pishiring.

Qatlama Patir tayyor!🤗
Uni nafaqat issiq ovqatlar bilan, balki oddiy choy bilan ham tanovul qilish mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "non_shirinkulcha": """Shirin kulcha 🥯
     Masalliqlar:🍱
Un: 1–1.2 kg
Sut: 500 ml
Tuxum: 2 dona
Sariyog‘ yoki margarin: 150–200 gr
Shakar: 150 gr
Xamirturush (droja): 10 gr yoki 1 osh qoshiq
Tuz: bir chimdim
Eritilgan sariyog‘: 100 gr (surish uchun)
Shakar: 100 gr (ustiga sepish uchun)

Tayyorlash usuli:🍱
1. Xamirni tayyorlash:
   - Sutni ilitib, sariyog‘ni eritib oling.
   - Sutga shakar va xamirturushni solib, yaxshilab aralashtiring.
   - Tuxum, tuz va unni solib, yumshoq xamir qorib oling. Xamir suvsiz, lekin elastik bo‘lishi lozim.
   - Xamirni issiqroq joyda ustini yopib, 1–1.5 soatga ko‘ptirishga qo‘ying.

2. Xamirni bo‘lish va tindirish:
   - Ko‘tarilgan xamirni 80–100 grammli zuvalachalarga bo‘ling.
   - Har bir zuvalachani ustini yopib, 10–15 daqiqa tindirib oling.

3. Xamirni yoyish va shakllantirish:
   - Har bir zuvalachani juda qalin bo‘lmagan qalinlikda yoying.
   - Eritilgan sariyog‘ surting va xamirni 3–4 qavat qilib bir chetdan taxlang.
   - Yarmidan boshlab pichoq bilan kesib, o‘rtasini oching. Shakl yurakka o‘xshashi kerak.

4. Tindirish:
   - Tayyorlangan yurak shaklidagi kulchalarni patnisga terib, issiq joyda 10–15 daqiqa oshirish uchun qoldiring.

5. Bezash va pishirish:
   - Har bir kulchaning ustiga tuxum surting va shakar sepib chiqing.
   - 200°C haroratdagi dimxonada tillarang bo‘lguncha 20–25 daqiqa davomida pishiring.

Murabbo yoki tvorogli variant:
- Zuvalachalarni yoyib, ichiga mevali shinni, murabbo yoki tvorogdan soling.
- Xamirni cheburek kabi yopib, chetlarini pichoq bilan ozgina qirqib chiqing.
- Tayyorlangan kulchalarni yuqoridagi usulda oshirib, ustiga tuxum surtib, 200°C haroratda qizartirib pishiring.

Pishgan shirin kulchalar issiq choy yoki qahva bilan nonushta uchun juda mos.🤗

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "non_moychechak": """Moychechak non 🥨
     Masalliqlar:🍱
Un: 1 kg
Sariyog‘ yoki margarin: 200 ml
Sut: 400 ml
Tuz: 1 osh qoshiq
Xamirturush: 10 gr yoki yarim osh qoshiq
Tuxum: 2 dona

Tayyorlash usuli:🍱
1. Xamirni tayyorlash:
   - Barcha masalliqlarni idishga solib, o‘rtacha yumshoqlikdagi xamir qorib oling.
   - Xamirni ustini yopib, issiq joyda 1–1.5 soat davomida oshirishga qo‘ying.

2. Xamirni bo‘lish va tindirish:
   - Oshgan xamirni bir xil vazndagi zuvalachalarga bo‘ling.
   - Har bir zuvalachani ustini yopib, yana 10–15 daqiqa tindirish uchun qoldiring.

3. Shakllantirish:
   - Har bir zuvalachani qo‘l yoki juva yordamida yoyib, o‘rtacha dumaloq shakl hosil qiling.
   - Xamirni 6 yoki 8 joyidan (xamir kattaligiga qarab) pichoq yordamida kesib, kesilgan uchlarini bir-biriga yopishtiring. Shakli moychechak guliga o‘xshash bo‘ladi.

4. Bezash va pishirish:
   - Tayyorlangan nonlarning ustiga tuxum yoki qatiq surtib chiqing.
   - Ustidan sedana yoki kunjut seping.
   - Nonlarni 200°C haroratdagi oldindan qizdirilgan dimxonaga qo‘yib, usti va osti qizarguncha pishiring (20–25 daqiqa).

Tavsiyalar:🤗
Moychechak noni har qanday taom bilan mazali bo‘ladi. Uni issiq choy yoki sho‘rva bilan dasturxonga tortiq qilishingiz mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "non_goshtli": """Go’shtli non 🍞
     Masalliqlar: (1 dona non uchun)🍱
Oshirilgan xamir: 160–180 gr
Go‘sht yoki qiyma: 50–60 gr
Piyoz: 40–50 gr
Ziravor va tuz: ta'bga ko‘ra

Tayyorlash usuli:🍱
1. Xamirni tayyorlash va oshirish:
   - Oldindan qorilgan xamirni oshirib, so‘ngra zuvalalarga bo‘lib oling.
   - Zuvalalarni 15–20 daqiqaga tindirishga qo‘ying.

2. Qiymaning tayyorlanishi:
   - To‘rtburchak shaklda mayda to‘g‘ralgan piyozni go‘sht yoki qiyma bilan aralashtiring.
   - Ta'bga ko‘ra ziravorlar va tuz qo‘shib, yaxshilab aralashtirib qayla holiga keltiring.

3. Non shakllantirish:
   - Tindirilgan zuvalalarni oddiy nonlarga qaraganda yupqaroq va kattaroq qilib yoying.
   - Yoyilgan xamirning o‘rtasiga qiymani xalqa shaklida qo‘ying.
   - Xamir chetlarini o‘rtasiga qaytarib, qiymani yopib chiqib, birlashtiring.
   - Keyin xamirni aylantirib, yopishtirilgan qismini ostiga qilib ag‘darib, o‘rtasini barmoq bilan yengil teshik qilib bosing.

4. Surtish va bezash:
   - Ustiga sut va suv aralashmasidan surting. Agar dimxonada pishirayotgan bo‘lsangiz, tuxum yoki qatiq surtishingiz mumkin.

5. Pishirish:
   - Tandirda: yuqori haroratda non qizarguncha yopiladi.
   - Dimxonada: 250°C haroratda usti va osti qizarguncha pishiriladi (taxminan 20–25 daqiqa).

Tavsiyalar:🤗
Pishgan go‘shtli nonni yangi uzilgan ko‘katlar yoki issiq choy bilan birga dasturxonga tortiq qilsangiz, yanada mazali bo‘ladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "non_patir": """Patir 🫓
     Masalliqlar:🍱
Un: 1 kg
Margarin: 80–100 gr
Eritilgan charvi yog‘: 80–100 gr
Tuz: 30 gr (1 osh qoshiq)
Xamirturush (droja): 10 gr (1 choy qoshiq)
Iliq suv: 450 ml

Tayyorlash usuli:🍱
1. Xamir qorish:
   - Iliq suvga eritilgan margarin va charvi yog‘ini qo‘shing.
   - Alohida idishda un, tuz va xamirturushni aralashtiring.
   - Aralashmani asta-sekinlik bilan yog‘li suyuqlikka qo‘shib, yaxshilab yumshoq xamir qorib oling.
   - Xamirni issiqroq joyda 1 soatga tindirib, oshishiga qo‘yib qo‘ying.

2. Zuvalalarga bo‘lish:
   - Oshgan xamirni 140–150 gr lik bo‘laklarga bo‘lib, zuvalalar hosil qiling.
   - Zuvalalarni ustini nam latta bilan yopib, yana 10–15 daqiqa tindiring.

3. Non shakllantirish:
   - Zuvalalarni qo‘llar bilan tekis yoyib, parkash shaklini bering.
   - Yoyilgan xamirda barmoq izlari qolmasligiga e'tibor bering.
   - Non o‘rtasiga chekich (chakich) bilan belgi bering va quruq sutdan tayyorlangan suyuqlik (1 osh qoshiq quruq sut + 2 osh qoshiq suv) surting.

4. Bezatish:
   - Ustiga sedana yoki kunjut sepib chiqing.

5. Pishirish:
   - Tandirda: Patirlarni qizib turgan tandirga yopib, qizarguncha pishiring.
   - Dimxona (duxovka): 220–240°C haroratda patirlarning usti va osti tillarang tusga kirguncha 20–25 daqiqa davomida pishiring.

Tavsiyalar:🤗
- Pishgan patirlarni yangi uzilgan ko‘katlar, issiq choy yoki sho‘rvalar bilan iste'mol qilish mazali bo‘ladi.
- Patirlar faqat taom bilan emas, choy bilan ham alohida mazali.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "non_lochira": """Lochira patir 🫓
     Masalliqlar:🍱
Un: 1 kg
Sut: 450 ml
Charvi va eritilgan sariyog‘: 120 gr
Tuz: 30 gr (1 osh qoshiq)
Soda: 1-2 chimdim
Xamirturush (droja): 1-2 chimdim
Ustiga surtish uchun tuxum: 1 dona
Bezatish uchun: Sedana yoki kunjut

Tayyorlash usuli:🍱
1. Xamir qorish:
   - Sutni ilitib, unga eritilgan charvi va sariyog‘ni qo‘shing.
   - Tuz, soda va drojani qo‘shib, yaxshilab aralashtiring.
   - Unni asta-sekin qo‘shib, o‘rtacha qattiqlikda xamir qorib oling.
   - Xamirni 15–20 daqiqaga tindirish uchun ustini yopib qo‘ying.

2. Zuvalalarga bo‘lish:
   - Xamirni 4-5 bo‘laklarga bo‘ling.
   - Har bir bo‘lakni zuvalaga aylantirib, yana 10–15 daqiqa tindiring.

3. Shakllantirish:
   - Zuvalani juva yordamida dumaloq shaklda yoyib chiqing.
   - Sirli lagan yoki likopchaga ozroq yog‘ surtib, yoyilgan xamirni joylashtiring.
   - Xamir yuzasini tekislang va chekich yordamida har yeridan urib chiqib, havo chiqishini ta'minlang.
   - Chetlarini chimchilab jimjima usulida shakl bering.

4. Bezatish:
   - Xamir ustiga tuxum surtib, sedana yoki kunjut sepib chiqing.

5. Pishirish:
   - 180°C darajada qizdirilgan dimxonada (duxovka) patirning usti va osti tillarang tusga kirguncha pishiring (20–25 daqiqa).

Tavsiyalar:🤗
- Lochira patirlar bayram dasturxoni yoki maxsus marosimlarning ajralmas qismi bo‘lib, issiq holida yanada mazali bo‘ladi.
- Bu patirlarni issiq choy yoki milliy taomlar bilan iste'mol qilishni tavsiya etamiz.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "non_obinon": """Obi non 🍞
     Masalliqlar:🍱
Un: 1 kg
Tuz: 30 gr (1 osh qoshiq)
Xamirturush (droja): 10 gr (1 kichik qadoqlangan paketcha)
Iliq suv: 620–640 ml

Tayyorlash usuli:🍱
1. Xamir tayyorlash:
   - Iliq suvga xamirturushni eritib qo'shing.
   - Un, tuz va eritilgan xamirturushni aralashtirib, yumshoq xamir qorib oling.
   - Yaxshi qorilgan xamirni 15–20 daqiqa tindirish uchun iliq joyda usti yopiq holda qoldiring.
   - Xamirning yaxshi qorilganini bilish uchun unda mayda pufakchalar hosil bo'lishi kerak.

2. Zuvalalarga bo‘lish:
   - Tayyor xamirni 140–150 gr lik bo‘laklarga bo‘lib, zuvalalar hosil qiling.
   - Zuvalalarni ustini nam latta bilan yopib, yana 10–15 daqiqa tindiring.

3. Non shakllantirish:
   - Zuvalalarni qo‘llar bilan tekis yoyib, parkash shaklini bering.
   - Yoyilgan xamirda barmoq izlari qolmasligiga e'tibor bering.
   - Non o‘rtasiga chekich (chakich) bilan belgi bering va quruq sutdan tayyorlangan suyuqlik (1 osh qoshiq quruq sut + 2 osh qoshiq suv) surting.

4. Bezatish:
   - Ustiga sedana yoki kunjut sepib chiqing. Bu nafaqat nonning husniga husn qo‘shadi, balki mazasini ham oshiradi.

5. Pishirish:
   - Tandir haroratini 300°C dan yuqoriga yetkazing.
   - Nonlarni gazna yordamida tandirga yopishtiring.
   - Nonlarni 3–5 daqiqa davomida pishiring.

6. Dasturxonga tortish:
   - Pishgan obi nonlar dasturxoningiz ko‘rkini oshiradi va istalgan taom bilan iste’mol qilish uchun juda mos keladi.

Tavsiyalar:🤗
- Tandir yo‘q bo‘lsa: Dimxona (duxovka)da ham obi nonni 220–250°C haroratda pishirib olish mumkin.
- Foydali qo'shimcha: Sedana va kunjut sog‘liq uchun foydali bo‘lib, nonni mazaliroq qiladi.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "non_qatlama": """Qatlama🫓
     Masalliqlar:🍱
Xamiriga:
Un — 0.5 kg
Sariyog‘ — 100-120 gr
Tuz — 1 choy qoshiq
Shakar — 1 choy qoshiq
Suv yoki sut — 240-260 ml

Ichiga:
Sariyog‘ — 100 gr
Qaymoq — 100 gr

Tayyorlash usuli:🍱
1. Xamir tayyorlash:
   - Xamirni tayyorlash uchun, avval tuzni suvda eritib oling.
   - So‘ngra, eritilgan sariyog‘ va shakarni qo‘shing, aralashtiring.
   - O‘rta yumshoqlikda xamirni qorib, uni usti yopiq joyda tindirib qo‘ying.

2. Ichiga tayyorlash:
   - Sariyog‘ni alohida idishda olovda eritib oling.
   - Qaymoqni yaxshilab iylab oling.

3. Xamirni yoyish:
   - Xamirni yupqa qilib yoying. E'tibor bering, xamir qanchalik yupqa bo‘lsa, qatlamlar shunchalik chiroyli bo‘lib chiqadi.
   - Yoyilgan xamirning ustiga tayyorlagan sariyog‘ va qaymoq aralashmasini teng miqdorda surting.

4. Tasmalarga bo‘lish:
   - Yoyilgan xamirni taxminan 3 sm kenglikdagi tasmachalar shaklida kesing.
   - Tasmalarni bir uchidan chap tomonga yig‘ib, ikkinchi qo‘lingiz bilan tortib borib, xamirni yanada yupqalashtiring.
   - Taxminan bir yarim tasmadan bitta zuvalacha tayyor bo‘ladi.

5. Qatlamalar yasash:
   - Tayyorlangan zuvalachalarni kulcha yasagandek, doiralar shaklida yoyib chiqing.
   - Qatlamalarni pishirish uchun issiq yog‘ga joylashtiring. Ikkala tomonini ham qizartirib, so‘ngra likopchaga yoki boshqa kattaroq idishga chiroyli qilib tering.

6. Bezash va pishirish:
   - Biroz sovugach, ustiga shakar seping.
   - Qatlama istalgan qo‘shimcha bilan, masalan, qaymoq, asal, murabbo yoki boshqa narsalar bilan dasturxonga tortiq qilishingiz mumkin.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
""",

    "non_jizzali": """Jizzali patir 🫓
Masalliqlar:🍱
Xamir uchun:
Un — 1 kg
Tuz — 30 gr yoki 1 osh qoshiq
Xamirturush (droja) — 10 gr yoki 1 choy qoshiq
Sut yoki suv — 550-600 ml

Qaylasi uchun:
Piyoz — 2-3 bosh
Ko‘k piyoz — 1-2 bog‘
Jizza — ta'bga ko‘ra
Tuz — ta'bga ko‘ra
Qora murch — ta'bga ko‘ra
Istasangiz, o‘simlik yog‘i qo‘shishingiz ham mumkin

Tayyorlash usuli:🍱
1. Xamir tayyorlash:
   - Un, tuz, xamirturush va iliq sut yoki suvni aralashtirib yumshoq xamir qoriladi.
   - Ustini yopib, iliqroq joyda oshguncha tindiriladi.

2. Qayla tayyorlash:
   - Piyoz, ko‘k piyoz va jizzani mayda qilib to‘g‘rang.
   - Tuz va qora murch qo‘shib yaxshilab aralashtiring.
   - Agar xohlasangiz, ozgina o‘simlik yog‘i ham qo‘shishingiz mumkin.

3. Zuvala yasash:
   - Oshgan xamirni 200-220 grammlik bo‘laklarga bo‘lib, zuvalachalar yasang.
   - Zuvalachalarni ustini yopib, 10-15 daqiqa davomida tindiring.

4. Xamirni yoyish va qayla solish:
   - Har bir zuvalachani qo‘l yoki jo‘va yordamida yoyib chiqing.
   - Xamirning yuzasiga ozgina o‘simlik yog‘i surting.
   - Tayyorlangan piyoz va jizzali qayladan solib, xamirni rulet shaklida o‘rang.
   - O‘ralgan xamirning ikki uchini o‘rtaga yig‘ib qo‘yib, yana 5-10 daqiqa davomida tindiring.

5. Patirni shakllantirish:
   - Tingan xamirni qo‘l yoki jo‘va yordamida yumaloq shaklda yoyib chiqing.
   - O‘rtasiga chekich bilan naqsh uring.

6. Pishirish:
   - Patirning yuzasiga qatiq, tuxum yoki sutli suyuqlik surting.
   - Ta'bga ko‘ra sedana yoki kunjut sepib chiqing.
   - 180-190 darajali dimxonada (duxovka) usti qizarguncha pishiring.

Yoqimli ishtaha!🍽️😋
Yordam bera olgan boʻlsam hursandman.
"""})

# ---------------------- Matn uzun bo'lganda bo'lib yuborish funktsiyasi -------------
async def send_long_text_in_chunks(text, chat_id, context, chunk_size=3500):
    """
    Telegram cheklovi sababli xabarni 4096 belgidan katta yuborolmaymiz.
    Xavfsiz tomoni uchun 3500 belgi atrofida bo'lib yuboriladi.
    """
    start = 0
    last_text_id = None
    while start < len(text):
        end = start + chunk_size
        sent_message = await context.bot.send_message(chat_id=chat_id, text=text[start:end])
        last_text_id = sent_message.message_id
        start = end
    return last_text_id

# ========================== START / BOSHLASH KOMANDASI ===========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # 3 tilda xush kelibsiz matni
    text = (
        "O'zbekcha:\n"
        "Assalomu alaykum!☺️ Sog'lom turmush tarzini targ'ib qiluvchi botga xush kelibsiz!\n"
        "Iltimos, o'zingizga qulay tilni tanlang.\n\n"

        "Русский:\n"
        "Ассаламу алайкум!☺️ Добро пожаловать в бота, продвигающего здоровый образ жизни!\n"
        "Пожалуйста, выберите удобный для вас язык.\n\n"

        "English:\n"
        "Assalamu alaykum!☺️ Welcome to the bot promoting a healthy lifestyle!\n"
        "Please select your preferred language."
    )

    # Tugmalar ham 3 tilda
    keyboard = [
        [
            InlineKeyboardButton("O'zbekcha 🇺🇿", callback_data='lang_uz'),
            InlineKeyboardButton("Русский 🇷🇺", callback_data='lang_ru'),
            InlineKeyboardButton("English 🇺🇸", callback_data='lang_en')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


# ===================== TIL TANLASH CALLBACK ===============================
async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split('_')[1]  # masalan 'uz', 'ru', 'en'
    context.user_data['lang'] = lang

    # 3 tilda xabar
    messages = {
        'uz': "Til tanlandi: O'zbekcha. Keling, boshlaymiz!🤗\nYoshingiz, bo'yingiz (sm) va vazningizni (kg) kiriting (masalan: 25, 175, 70).",
        'ru': "Вы выбрали русский язык. Давайте начнём!🤗\nВведите ваш возраст, рост (см) и вес (кг) (например: 25, 175, 70).",
        'en': "You selected English. Let's start!🤗\nPlease enter your age, height (cm), and weight (kg) (e.g., 25, 175, 70)."
    }

    await query.edit_message_text(text=messages[lang])


# ==================== FOYDALANUVCHI MA'LUMOTLARINI QABUL QILISH ====================
async def handle_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if 'lang' not in context.user_data:
        await update.message.reply_text("Iltimos, /start dan boshlang.")
        return

    lang = context.user_data['lang']

    try:
        # Masalan: "25, 175, 70"
        age, height, weight = map(int, update.message.text.replace(' ', '').split(','))
        context.user_data.update({'age': age, 'height': height, 'weight': weight})

        # BMI, BMR, suv hisobi
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        bmr = 10 * weight + 6.25 * height - 5 * age + 5  # erkaklar uchun formula
        daily_water_liters = weight * 30 / 1000

        # BMI ga ko'ra tavsiya matnlari - 3 tilda
        bmi_status_text = {
            'uz': (
                "Sizning vazningiz kam. Vazn olish tavsiya etiladi.🙂" if bmi < 18.5 else
                "Sizning vazningiz sog'lom darajada.☺️" if 18.5 <= bmi < 24.9 else
                "Sizning vazningiz yuqori. Vazn yo'qotish tavsiya etiladi.🙃" if 25 <= bmi < 29.9 else
                "Sizda ortiqcha vazn bor. Mutaxassisga murojaat qiling.😌"
            ),
            'ru': (
                "Ваш вес недостаточный. Рекомендуется набрать вес.🙂" if bmi < 18.5 else
                "Ваш вес в норме.☺️" if 18.5 <= bmi < 24.9 else
                "Ваш вес выше нормы. Рекомендуется похудеть.🙃" if 25 <= bmi < 29.9 else
                "У вас лишний вес. Обратитесь к специалисту.😌"
            ),
            'en': (
                "Your weight is below normal. Weight gain is recommended.🙂" if bmi < 18.5 else
                "Your weight is in the healthy range.☺️" if 18.5 <= bmi < 24.9 else
                "Your weight is above normal. Weight loss is recommended.🙃" if 25 <= bmi < 29.9 else
                "You are overweight. Consult a specialist.😌"
            )
        }

        # Zararlı va foydali ovqatlar ro'yxati - 3 tilda
        harmful_text = {
            'uz': (
                "Zararli ichimliklar va taomlardan saqlaning:🤗\n"
                "- Shirin gazlangan ichimliklar\n"
                "- Spirtli ichimliklar\n"
                "- Haddan tashqari yog'li va qovurilgan ovqatlar\n"
                "- Ortiqcha tuz va shakar iste'moli\n\n"
                "Foydali odatlar:\n"
                "- Oddiy suv iching\n"
                "- Ko'katlar va mevalar iste'mol qiling\n"
                "- Sog'lom yog'lar (zaytun moyi va h.k)."
            ),
            'ru': (
                "Избегайте вредных напитков и пищи:🤗\n"
                "- Сладкие газированные напитки\n"
                "- Алкогольные напитки\n"
                "- Жирная и жареная еда\n"
                "- Избыточное употребление соли и сахара\n\n"
                "Полезные привычки:\n"
                "- Пейте чистую воду\n"
                "- Ешьте зелень и фрукты\n"
                "- Используйте здоровые жиры (оливковое масло и т.д.)."
            ),
            'en': (
                "Avoid harmful drinks and foods:🤗\n"
                "- Sugary fizzy drinks\n"
                "- Alcoholic beverages\n"
                "- Excessively fatty and fried foods\n"
                "- Excessive salt and sugar consumption\n\n"
                "Healthy habits:\n"
                "- Drink plain water\n"
                "- Eat greens and fruits\n"
                "- Use healthy fats (olive oil, etc)."
            )
        }

        # Foydalanuvchiga umumiy xabar
        summary_text = {
            'uz': f"Sizning BMI: 😊{bmi:.2f}. {bmi_status_text[lang]}\n" \
                  f"Kunlik kaloriya ehtiyojingiz (BMR): {bmr:.2f} kkal.\n" \
                  f"Kunlik suv iste'moli: {daily_water_liters:.1f} litr.\n\n" \
                  f"{harmful_text[lang]}",

            'ru': f"Ваш ИМТ: 😊{bmi:.2f}. {bmi_status_text[lang]}\n" \
                  f"Суточная норма калорий (BMR): {bmr:.2f} ккал.\n" \
                  f"Рекомендуемое количество воды: {daily_water_liters:.1f} литра.\n\n" \
                  f"{harmful_text[lang]}",

            'en': f"Your BMI: 😊{bmi:.2f}. {bmi_status_text[lang]}\n" \
                  f"Daily calorie needs (BMR): {bmr:.2f} kcal.\n" \
                  f"Daily water intake: {daily_water_liters:.1f} liters.\n\n" \
                  f"{harmful_text[lang]}"
        }

        full_text = summary_text[lang]
        if len(full_text) > 3500:
            last_text_id = await send_long_text_in_chunks(full_text, update.effective_chat.id, context)
            # "Ortga" tugmasini faqat oxirgi matn bo'lagi ostiga qo'yish uchun alohida yuboramiz
            sent_back = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="...",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ortga", callback_data='back_to_taomlar')]])
            )
            context.user_data['last_text_id'] = sent_back.message_id
        else:
            sent_text = await update.message.reply_text(full_text)
            context.user_data['last_text_id'] = sent_text.message_id

        # Maqsad tanlash tugmalari
        goal_buttons = {
            'uz': ["👉Vazn olish👈", "👉Vazn yo'qotish👈", "👉Vazn saqlash👈"],
            'ru': ["👉Набрать вес👈", "👉Похудеть👈", "👉Сохранить вес👈"],
            'en': ["👉Gain weight👈", "👉Lose weight👈", "👉Maintain weight👈"]
        }
        g_btns = goal_buttons[lang]
        keyboard = [
            [InlineKeyboardButton(g_btns[0], callback_data='goal_gain')],
            [InlineKeyboardButton(g_btns[1], callback_data='goal_lose')],
            [InlineKeyboardButton(g_btns[2], callback_data='goal_maintain')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        choose_text = {
            'uz': "Maqsadingizni tanlang:👇",
            'ru': "Выберите цель:👇",
            'en': "Choose your goal:👇"
        }

        await update.message.reply_text(choose_text[lang], reply_markup=reply_markup)

    except ValueError:
        # Xatolik xabarlari ham 3 tilda
        errors = {
            'uz': "Format xato. (Misol: 25, 175, 70).",
            'ru': "Неверный формат. (Например: 25, 175, 70).",
            'en': "Invalid format. (Example: 25, 175, 70)."
        }
        await update.message.reply_text(errors[lang])


# ===================== MAQSAD TANLASH ==========================
async def goal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    goal_type = query.data.split('_')[1]  # gain, lose, maintain
    user_id = query.from_user.id
    lang = context.user_data['lang']

    # Tavsiyalar (gain/lose/maintain) - 3 tilda
    exercises_info = {
        'gain': {
            'uz': ("🤗Mashg'ulot: Kuch mashg'ulotlari (gantel, og'irliklar):\n"
                   "- Foyda: Mushaklarni kuchaytiradi, vaznni ko'paytiradi.\n"
                   "- Vaqt: 30-40 daqiqa har kuni, haftada 4-5 kun.\n"
                   "- Kaloriya sarfi: ~150-200 kkal (30 daqiqada).\n"
                   "- Ehtiyotkorlik: Bel og'rig'i bo'lganlar ehtiyot bo'lsin.\n"
                   "Quyida foydali taomlarning retseptlari berilgan. Ko'rish uchun 'Taomlar retsepti' tugmasini bosing."),
            'ru': ("🤗Силовые тренировки (гантели, штанга):\n"
                   "- Польза: Укрепляет мышцы, способствует набору веса.\n"
                   "- Время: 30-40 минут в день, 4-5 раз в неделю.\n"
                   "- Калории: ~150-200 ккал за 30 мин.\n"
                   "- Осторожность: При боли в спине будьте внимательны.\n"
                   "Ниже приведены рецепты полезных блюд. Нажмите кнопку «Рецепты блюд», чтобы их посмотреть."),
            'en': ("🤗Strength training (dumbbells, weights):\n"
                   "- Benefit: Builds muscle, increases weight.\n"
                   "- Time: 30-40 min daily, 4-5 times/week.\n"
                   "- Calories: ~150-200 kcal in 30 min.\n"
                   "- Caution: Watch out for back pain.\n"
                   "Below are recipes for healthy dishes. Click the 'Dish Recipes' button to view them.")
        },
        'lose': {
            'uz': ("🤗Mashg'ulot: Kardio (yugurish, velosiped):\n"
                   "- Foyda: Yog'ni yo'qotadi, yurakni kuchaytiradi.\n"
                   "- Vaqt: 40-60 daqiqa kuniga, haftada 5-6 kun.\n"
                   "- Kaloriya sarfi: ~250-300 kkal (30 daq).\n"
                   "- Ehtiyotkorlik: Yurak muammosi bo'lganlar ehtiyot bo'lsin.\n"
                   "Quyida foydali taomlarning retseptlari berilgan. Ko'rish uchun 'Taomlar retsepti' tugmasini bosing."),
            'ru': ("🤗Кардио (бег, велосипед):\n"
                   "- Сжигает жир, укрепляет сердце.\n"
                   "- 40-60 мин в день, 5-6 раз в неделю.\n"
                   "- Калории: ~250-300 ккал за 30 мин.\n"
                   "- Осторожность: При сердечных болезнях осторожнее.\n"
                   "Ниже приведены рецепты полезных блюд. Нажмите кнопку «Рецепты блюд», чтобы их посмотреть."),
            'en': ("🤗Cardio (running, cycling):\n"
                   "- Burns fat, improves heart health.\n"
                   "- 40-60 min/day, 5-6 days/week.\n"
                   "- ~250-300 kcal per 30 min.\n"
                   "- Caution: heart conditions.\n"
                   "Below are recipes for healthy dishes. Click the 'Dish Recipes' button to view them.")
        },
        'maintain': {
            'uz': ("🤗Kombinatsion mashg'ulotlar (kardio+kuch):\n"
                   "- Foyda: Vaznni saqlaydi.\n"
                   "- 30-40 daqiqa kuniga, 4-5 kun/hafta.\n"
                   "- ~200-250 kkal(30 daqiqa).\n"
                   "- Ehtiyotkorlik: Yaxshi dam olish.\n"
                   "Quyida foydali taomlarning retseptlari berilgan. Ko'rish uchun 'Taomlar retsepti' tugmasini bosing."),
            'ru': ("🤗Комбинированная тренировка (кардио+силовые):\n"
                   "- Помогает держать вес.\n"
                   "- 30-40 мин в день, 4-5 раз в неделю.\n"
                   "- ~200-250 ккал за 30 мин.\n"
                   "- Отдых обязателен.\n"
                   "Ниже приведены рецепты полезных блюд. Нажмите кнопку «Рецепты блюд», чтобы их посмотреть."),
            'en': ("🤗Combination (cardio+strength):\n"
                   "- Maintains weight.\n"
                   "- 30-40 min/day, 4-5 times/week.\n"
                   "- ~200-250 kcal/30 min.\n"
                   "- Ensure rest.\n"
                   "Below are recipes for healthy dishes. Click the 'Dish Recipes' button to view them.")
        }
    }

    text_to_send = exercises_info[goal_type][lang]

    # "Taomlar retsepti" tugmasi - 3 tilda
    recipe_button = {
        'uz': "👉Taomlar retsepti👈",
        'ru': "👉Рецепты👈",
        'en': "👉Recipes👈"
    }

    keyboard = [[InlineKeyboardButton(recipe_button[lang], callback_data='recipes')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text_to_send, reply_markup=reply_markup)


# =========================== ASOSIY "TAOMLAR" BO'LIMI ===========================
async def show_main_taomlar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """‘recipes’ callback bosilganda chaqiramiz."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang = context.user_data['lang']

    # 3 tilda sarlavha
    text_dict = {
        'uz': "Taomlar bo‘limi. Qaysi bo‘limni tanlaysiz?🤔",
        'ru': "Раздел блюд. Какое блюдо выберете?🤔",
        'en': "Recipe categories. Which one do you choose?🤔"
    }

    # Bo‘limlar tugmalari (barchasi bir xil, faqat matnlari 3 tilda yozilishi mumkin)
    # Ushbu tugmalar callback_data bilan ishga tushadi: cat_suyuq, cat_quyuq, ...
    keyboard = [
        [InlineKeyboardButton("Suyuq taomlar🍲", callback_data='cat_suyuq')],
        [InlineKeyboardButton("Quyuq taomlar🍝", callback_data='cat_quyuq')],
        [InlineKeyboardButton("Salatlar🥗", callback_data='cat_salatlar')],
        [InlineKeyboardButton("Pishiriqlar🥧", callback_data='cat_pishiriqlar')],
        [InlineKeyboardButton("Shirinliklar🍩", callback_data='cat_shirinliklar')],
        [InlineKeyboardButton("Ichimliklar🍹", callback_data='cat_ichimliklar')],
        [InlineKeyboardButton("Tortlar🍰", callback_data='cat_tortlar')],
        [InlineKeyboardButton("Nonlar🍞", callback_data='cat_nonlar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text_dict[lang], reply_markup=reply_markup)


# ======================== Yordamchi funksiyasi ===================
async def show_dish_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat = query.data.split('_')[1]  # suyuq, quyuq, salatlar...
    await show_dish_categories_logic(cat, query, context)


async def show_dish_categories_logic(cat: str, query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
    """
    Ushbu logic bo‘lim nomi (cat)ga qarab, tegishli keyboard va sarlavhani qaytaradi.
    masalan cat='suyuq', 'quyuq', 'salatlar', ...
    """
    user_id = query.from_user.id
    lang = context.user_data.get('lang', 'uz')  # Default 'uz'

    category_titles = {
        'uz': {
            'suyuq': "Suyuq taomlar:🍲",
            'quyuq': "Quyuq taomlar:🍝",
            'salatlar': "Salatlar:🥗",
            'pishiriqlar': "Pishiriqlar:🥧",
            'shirinliklar': "Shirinliklar:🍩",
            'ichimliklar': "Ichimliklar:🍹",
            'tortlar': "Tortlar:🍰",
            'nonlar': "Nonlar:🍞"
        },
        'ru': {
            'suyuq': "Супы:🍲",
            'quyuq': "Тушеные блюда:🍝",
            'salatlar': "Салаты:🥗",
            'pishiriqlar': "Выпечка:🥧",
            'shirinliklar': "Десерты:🍩",
            'ichimliklar': "Напитки:🍹",
            'tortlar': "Торты:🍰",
            'nonlar': "Хлеба:🍞"
        },
        'en': {
            'suyuq': "Soups:🍲",
            'quyuq': "Stews:🍝",
            'salatlar': "Salads:🥗",
            'pishiriqlar': "Baked Goods:🥧",
            'shirinliklar': "Desserts:🍩",
            'ichimliklar': "Drinks:🍹",
            'tortlar': "Cakes:🍰",
            'nonlar': "Breads:🍞"
        }
    }

    # Define the keyboard based on category
    if cat == "suyuq":
        text_label = category_titles[lang]['suyuq']
        keyboard = [
            [InlineKeyboardButton("Ko'za sho'rva", callback_data='dish_kosashorva')],
            [InlineKeyboardButton("Dumbulli dimlama", callback_data='dish_dumbullidimlama')],
            [InlineKeyboardButton("Piyozli sho'rva", callback_data='dish_piyozlishorva')],
            [InlineKeyboardButton("Suyuq norin", callback_data='dish_suyuqnorin')],
            [InlineKeyboardButton("Uyg'ur lag'mon", callback_data='dish_uygurlagmon')],
            [InlineKeyboardButton("Moxora", callback_data='dish_moxora')],
            [InlineKeyboardButton("Go'ja", callback_data='dish_goja')],
            [InlineKeyboardButton("Lag'mon", callback_data='dish_lagmon')],
            [InlineKeyboardButton("Sabzavotli do'lma", callback_data='dish_sabzavotd')],
            [InlineKeyboardButton("Mantili sho'rva", callback_data='dish_mantilishorva')],
            [InlineKeyboardButton("Firkadelkali sho'rva", callback_data='dish_firkadelkali')],
            [InlineKeyboardButton("Kosa dimlama", callback_data='dish_kosadimlama')],
            [InlineKeyboardButton("Tuxum do'lma", callback_data='dish_tuxumdolma')],
            [InlineKeyboardButton("Mastava", callback_data='dish_mastava')],
            [InlineKeyboardButton("Chuchvara", callback_data='dish_chuchvara')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "quyuq":
        text_label = category_titles[lang]['quyuq']
        keyboard = [
            [InlineKeyboardButton("Andijon manti", callback_data='dish_andijonmanti')],
            [InlineKeyboardButton("Spagetti", callback_data='dish_spagetti')],
            [InlineKeyboardButton("Qovurma lag'mon", callback_data='dish_qovurmala')],
            [InlineKeyboardButton("Dimlama", callback_data='dish_dimlama')],
            [InlineKeyboardButton("Besh barmoq", callback_data='dish_beshbarmoq')],
            [InlineKeyboardButton("Bibimbap", callback_data='dish_bibimbap')],
            [InlineKeyboardButton("Do'lma", callback_data='dish_quyuqdolma')],
            [InlineKeyboardButton("Choyxona palov", callback_data='dish_choyxona')],
            [InlineKeyboardButton("Gulxonim", callback_data='dish_gulxonim')],
            [InlineKeyboardButton("Bayramona osh va ayron", callback_data='dish_bayramona')],
            [InlineKeyboardButton("Grechka palov", callback_data='dish_grechkapalov')],
            [InlineKeyboardButton("Turkcha ratatuy", callback_data='dish_turkcharatatuy')],
            [InlineKeyboardButton("Balish", callback_data='dish_balish')],
            [InlineKeyboardButton("Go'shli rulet", callback_data='dish_goshlirulet')],
            [InlineKeyboardButton("Shivit oshi", callback_data='dish_shivit')],
            [InlineKeyboardButton("Non palov", callback_data='dish_nonpalov')],
            [InlineKeyboardButton("Kartoshka do'lma", callback_data='dish_kartoshkadolma')],
            [InlineKeyboardButton("Dumbul palov", callback_data='dish_dumbulpalov')],
            [InlineKeyboardButton("Teftel", callback_data='dish_teftel')],
            [InlineKeyboardButton("Sarimsoqli kartoshka", callback_data='dish_sarimsoqli')],
            [InlineKeyboardButton("Begodi", callback_data='dish_begodi')],
            [InlineKeyboardButton("Baliqli kotlet", callback_data='dish_baliqlikotlet')],
            [InlineKeyboardButton("Jigar kabob", callback_data='dish_jigarkabob')],
            [InlineKeyboardButton("Qozon kabob", callback_data='dish_qozonkabob')],
            [InlineKeyboardButton("Qiymali kabob", callback_data='dish_qiymalikabob')],
            [InlineKeyboardButton("Tandir kabob", callback_data='dish_tandirkabob')],
            [InlineKeyboardButton("Tovuq kabob", callback_data='dish_tovuqkabob')],
            [InlineKeyboardButton("Namangan kabob", callback_data='dish_namangankabob')],
            [InlineKeyboardButton("Norin", callback_data='dish_norin')],
            [InlineKeyboardButton("Xasip", callback_data='dish_xasip')],
            [InlineKeyboardButton("Tuxum Barak", callback_data='dish_tuxumbarak')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "salatlar":
        text_label = category_titles[lang]['salatlar']
        keyboard = [
            [InlineKeyboardButton("Achchiq chuchuk salat", callback_data='dish_achchiqchuchuk')],
            [InlineKeyboardButton("Bodring va brinzali salat", callback_data='dish_bodringbrinza')],
            [InlineKeyboardButton("Karam va pomidorli salat", callback_data='dish_karampomidor')],
            [InlineKeyboardButton("Gruzincha salat", callback_data='dish_gruzincha')],
            [InlineKeyboardButton("Qarsildoq salat", callback_data='dish_qarsildoq')],
            [InlineKeyboardButton("Suzmali salat", callback_data='dish_suzmali')],
            [InlineKeyboardButton("Penchuza salat", callback_data='dish_penchuza')],
            [InlineKeyboardButton("Mandarin salat", callback_data='dish_mandarin')],
            [InlineKeyboardButton("Tovuqli salat", callback_data='dish_tovuqlisalat')],
            [InlineKeyboardButton("Smak salat", callback_data='dish_smak')],
            [InlineKeyboardButton("Ozdiruvchi salat", callback_data='dish_ozdiruvchi')],
            [InlineKeyboardButton("Mevali salat", callback_data='dish_mevali')],
            [InlineKeyboardButton("Braslet salat", callback_data='dish_braslet')],
            [InlineKeyboardButton("Qotgan nonli salat", callback_data='dish_qotgannonli')],
            [InlineKeyboardButton("Go'shtli salat", callback_data='dish_goshtlisa')],
            [InlineKeyboardButton("Karamli salat", callback_data='dish_karamli')],
            [InlineKeyboardButton("Olivye", callback_data='dish_olivye')],
            [InlineKeyboardButton("Tovuqli olivye", callback_data='dish_tovuqiolivye')],
            [InlineKeyboardButton("Bodring salat", callback_data='dish_bodringsalat')],
            [InlineKeyboardButton("Shanxaycha salat", callback_data='dish_shanxay')],
            [InlineKeyboardButton("Qush uyali salat", callback_data='dish_qushuyali')],
            [InlineKeyboardButton("Toshkentcha salat", callback_data='dish_toshkentsalat')],
            [InlineKeyboardButton("Portobello salat", callback_data='dish_portobello')],
            [InlineKeyboardButton("Ananas va tovuqli salat", callback_data='dish_ananas')],
            [InlineKeyboardButton("Sezar salat", callback_data='dish_sezar')],
            [InlineKeyboardButton("Bodring va karamli salat", callback_data='dish_bodringkaram')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "pishiriqlar":
        text_label = category_titles[lang]['pishiriqlar']
        keyboard = [
            [InlineKeyboardButton("Turkcha burek", callback_data='dish_turkchaburek')],
            [InlineKeyboardButton("Go’shtli somsa", callback_data='dish_goshtlisomsa')],
            [InlineKeyboardButton("Yupqa", callback_data='dish_yupqa')],
            [InlineKeyboardButton("Qiymali quymoq", callback_data='dish_qiymaliquymoq')],
            [InlineKeyboardButton("Pishloqli cheburek", callback_data='dish_pishloqlicheburek')],
            [InlineKeyboardButton("Gumma", callback_data='dish_gumma')],
            [InlineKeyboardButton("Pahlava", callback_data='dish_pahlava')],
            [InlineKeyboardButton("Chak-chak", callback_data='dish_chakchak')],
            [InlineKeyboardButton("Turkcha pishiriq", callback_data='dish_turkchapishiriq')],
            [InlineKeyboardButton("Qozon somsa", callback_data='dish_qozonsomsa')],
            [InlineKeyboardButton("Sabzavotli somsa", callback_data='dish_sabzavotlisomsa')],
            [InlineKeyboardButton("Yurak somsa", callback_data='dish_yuraksomsa')],
            [InlineKeyboardButton("Qatlama somsa", callback_data='dish_qatlamasomsa')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "shirinliklar":
        text_label = category_titles[lang]['shirinliklar']
        keyboard = [
            [InlineKeyboardButton("Nisholda", callback_data='dish_nisholda')],
            [InlineKeyboardButton("Holvetar", callback_data='dish_holvetar')],
            [InlineKeyboardButton("Tvarogli krendel", callback_data='dish_tvaroglikr')],
            [InlineKeyboardButton("Shokoladli glazur", callback_data='dish_shokoglazur')],
            [InlineKeyboardButton("Bananli eskimo", callback_data='dish_bananlieskimo')],
            [InlineKeyboardButton("Jemli pirog", callback_data='dish_jemlipirog')],
            [InlineKeyboardButton("Tvarogli bulochka", callback_data='dish_tvoroglibulochka')],
            [InlineKeyboardButton("Malinali chizkeyk", callback_data='dish_malinalichizkeyk')],
            [InlineKeyboardButton("Bolqaymoq", callback_data='dish_bolqaymoq')],
            [InlineKeyboardButton("Murabboli pirog", callback_data='dish_murabbolipirog')],
            [InlineKeyboardButton("Asalli pirojniy", callback_data='dish_asallipirojniy')],
            [InlineKeyboardButton("Shaftolili muzqaymoq", callback_data='dish_shaftolilimizq')],
            [InlineKeyboardButton("Aylanay pirogi", callback_data='dish_aylanay')],
            [InlineKeyboardButton("Chumoli uyasi", callback_data='dish_chumoliuya')],
            [InlineKeyboardButton("Olchali pirog", callback_data='dish_olchali')],
            [InlineKeyboardButton("Shokoladli keks", callback_data='dish_shokokeks')],
            [InlineKeyboardButton("Asalli pechenye", callback_data='dish_asallipechenye')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "ichimliklar":
        text_label = category_titles[lang]['ichimliklar']
        keyboard = [
            [InlineKeyboardButton("Olmali choy", callback_data='drink_olmali')],
            [InlineKeyboardButton("Namatak sharbati", callback_data='drink_namatak')],
            [InlineKeyboardButton("Yalpizli limon choy", callback_data='drink_yalpizlimon')],
            [InlineKeyboardButton("Qulupnayli ichimlik", callback_data='drink_qulupnay')],
            [InlineKeyboardButton("Qovun sharbati", callback_data='drink_qovun')],
            [InlineKeyboardButton("Bodomli sut", callback_data='drink_bodomli')],
            [InlineKeyboardButton("Uzum sharbati", callback_data='drink_uzum')],
            [InlineKeyboardButton("Mevali sharbat", callback_data='drink_mevali')],
            [InlineKeyboardButton("Qatiq", callback_data='drink_qatiq')],
            [InlineKeyboardButton("Tarvuz sharbati", callback_data='drink_tarvuz')],
            [InlineKeyboardButton("Sabzi sharbati", callback_data='drink_sabzi')],
            [InlineKeyboardButton("Zira choy", callback_data='drink_zira')],
            [InlineKeyboardButton("Vitaminli ichimlik", callback_data='drink_vitaminli')],
            [InlineKeyboardButton("Moxito", callback_data='drink_moxito')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "tortlar":
        text_label = category_titles[lang]['tortlar']
        keyboard = [
            [InlineKeyboardButton("Praga torti", callback_data='tort_praga')],
            [InlineKeyboardButton("Napaleon torti", callback_data='tort_napaleon')],
            [InlineKeyboardButton("Zebra torti", callback_data='tort_zebra')],
            [InlineKeyboardButton("Pancho torti", callback_data='tort_pancho')],
            [InlineKeyboardButton("Medovik torti", callback_data='tort_medovik')],
            [InlineKeyboardButton("Frezye torti", callback_data='tort_frezye')],
            [InlineKeyboardButton("Karamel va yong’oqli tort", callback_data='tort_karamel')],
            [InlineKeyboardButton("Kita-kat torti", callback_data='tort_kitakat')],
            [InlineKeyboardButton("Bostoncha kremli tort", callback_data='tort_boston')],
            [InlineKeyboardButton("Bounty torti", callback_data='tort_bounty')],
            [InlineKeyboardButton("Pavlova torti", callback_data='tort_pavlova')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "nonlar":
        text_label = category_titles[lang]['nonlar']
        keyboard = [
            [InlineKeyboardButton("Qatlama patir", callback_data='non_qatlamapatir')],
            [InlineKeyboardButton("Shirin kulcha", callback_data='non_shirinkulcha')],
            [InlineKeyboardButton("Moychechak non", callback_data='non_moychechak')],
            [InlineKeyboardButton("Go’shtli non", callback_data='non_goshtli')],
            [InlineKeyboardButton("Patir", callback_data='non_patir')],
            [InlineKeyboardButton("Lochira patir", callback_data='non_lochira')],
            [InlineKeyboardButton("Obi non", callback_data='non_obinon')],
            [InlineKeyboardButton("Qatlama", callback_data='non_qatlama')],
            [InlineKeyboardButton("Jizzali patir", callback_data='non_jizzali')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    else:
        text_label = "Noma'lum bo‘lim."
        keyboard = [[InlineKeyboardButton("Ortga", callback_data='back_to_taomlar')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text_label, reply_markup=reply_markup)


# =========================== ASOSIY RETSEPT CALLBACK =============================
async def show_recipe_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data_key = query.data  # masalan dish_kosashorva, drink_olmali, tort_praga, non_qatlamapatir,...
    text_data = recipes_texts.get(data_key, "Bu taom (yoki ichimlik) bo'yicha ma'lumot topilmadi.")

    # Rasm yo'lini olish
    image_path = images_paths.get(data_key)

    # Orqaga qaytish callback aniqlash
    if data_key.startswith("dish_"):
        # dish_ so'zini aniqlaymiz
        if any(k in data_key for k in [
            "kosashorva", "dumbullidimlama", "piyozlishorva", "suyuqnorin", "uygurlagmon", "moxora", "goja",
            "lagmon", "sabzavotd", "mantilishorva", "firkadelkali", "kosadimlama", "tuxumdolma", "mastava", "chuchvara"
        ]):
            back_cat = "suyuq"
        elif any(k in data_key for k in [
            "andijonmanti", "spagetti", "qovurmala", "dimlama", "beshbarmoq", "bibimbap", "quyuqdolma",
            "choyxona", "gulxonim", "bayramona", "grechkapalov", "turkcharatatuy", "balish", "goshlirulet", "shivit",
            "nonpalov", "kartoshkadolma", "dumbulpalov", "teftel", "sarimsoqli", "begodi", "baliqlikotlet",
            "jigarkabob",
            "qozonkabob", "qiymalikabob", "tandirkabob", "tovuqkabob", "namangankabob", "norin", "xasip", "tuxumbarak"
        ]):
            back_cat = "quyuq"
        elif any(k in data_key for k in [
            "achchiqchuchuk", "bodringbrinza", "karampomidor", "gruzincha", "qarsildoq", "suzmali", "penchuza",
            "mandarin",
            "tovuqlisalat", "smak", "ozdiruvchi", "mevali", "braslet", "qotgannonli", "goshtlisa", "karamli", "olivye",
            "tovuqiolivye", "bodringsalat", "shanxay", "qushuyali", "toshkentsalat", "portobello", "ananas", "sezar",
            "bodringkaram"
        ]):
            back_cat = "salatlar"
        elif any(k in data_key for k in [
            "turkchaburek", "goshtlisomsa", "yupqa", "qiymaliquymoq", "pishloqlicheburek", "gumma", "pahlava",
            "chakchak",
            "turkchapishiriq", "qozonsomsa", "sabzavotlisomsa", "yuraksomsa", "qatlamasomsa"
        ]):
            back_cat = "pishiriqlar"
        elif any(k in data_key for k in [
            "nisholda", "holvetar", "tvaroglikr", "shokoglazur", "bananlieskimo", "jemlipirog", "tvoroglibulochka",
            "malinalichizkeyk", "bolqaymoq", "murabbolipirog", "asallipirojniy", "shaftolilimizq", "aylanay",
            "chumoliuya",
            "olchali", "shokokeks", "asallipechenye"
        ]):
            back_cat = "shirinliklar"
        else:
            back_cat = "suyuq"  # default

        # Back callback
        if data_key.startswith("dish_"):
            back_callback = f"back_to_category_{back_cat}"
        elif data_key.startswith("drink_"):
            back_callback = "back_to_category_ichimliklar"
        elif data_key.startswith("tort_") or data_key.startswith("drezden_"):
            back_callback = "back_to_category_tortlar"
        elif data_key.startswith("non_"):
            back_callback = "back_to_category_nonlar"
        else:
            back_callback = "back_to_taomlar"
    else:
        back_callback = "back_to_taomlar"

    # "Ortga" tugmasi uchun keyboard
    keyboard = [[InlineKeyboardButton("Ortga", callback_data=back_callback)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Rasm yuborish va message_id saqlash
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as img_file:
                sent_photo = await context.bot.send_photo(chat_id=user_id, photo=img_file)
            # `message_id`ni saqlash
            context.user_data['last_photo_id'] = sent_photo.message_id
        except Exception as e:
            logger.error(f"Rasm yuborishda xatolik: {e}")
            await context.bot.send_message(chat_id=user_id, text="Rasmni yuborishda xatolik yuz berdi.")
    else:
        logger.warning(f"Rasm topilmadi: {image_path}")
        await context.bot.send_message(chat_id=user_id, text="Rasm topilmadi.")

    # Matn yuborish va `message_id`ni saqlash
    if len(text_data) > 3500:
        last_text_id = await send_long_text_in_chunks(text_data, user_id, context)
        # "Ortga" tugmasini faqat oxirgi matn bo'lagi ostiga qo'yish uchun alohida yuboramiz
        sent_back = await context.bot.send_message(
            chat_id=user_id,
            text="...",
            reply_markup=reply_markup
        )
        context.user_data['last_text_id'] = sent_back.message_id
    else:
        sent_text = await context.bot.send_message(chat_id=user_id, text=text_data, reply_markup=reply_markup)
        context.user_data['last_text_id'] = sent_text.message_id


# ================== back_to_taomlar => show_main_taomlar_menu ====================
async def back_to_taomlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # So'nggi yuborilgan rasm xabarini o'chirish
    if 'last_photo_id' in context.user_data:
        try:
            await context.bot.delete_message(chat_id=user_id, message_id=context.user_data['last_photo_id'])
            del context.user_data['last_photo_id']
        except Exception as e:
            logger.error(f"Rasmni o'chirishda xatolik: {e}")

    # So'nggi yuborilgan matn xabarini o'chirish
    if 'last_text_id' in context.user_data:
        try:
            await context.bot.delete_message(chat_id=user_id, message_id=context.user_data['last_text_id'])
            del context.user_data['last_text_id']
        except Exception as e:
            logger.error(f"Matnni o'chirishda xatolik: {e}")

    # So'nggi yuborilgan umumiy xabarni o'chirish (agar mavjud bo'lsa)
    if 'last_message_id' in context.user_data:
        try:
            await context.bot.delete_message(chat_id=user_id, message_id=context.user_data['last_message_id'])
            del context.user_data['last_message_id']
        except Exception as e:
            logger.error(f"Umumiy xabarni o'chirishda xatolik: {e}")

    # Asosiy taomlar menyusini ko'rsatish
    await show_main_taomlar_menu(update, context)


# ============== Orqaga bo‘limga qaytish => back_to_category_suyuq, quyuq, ... =====
async def back_to_category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # So'nggi yuborilgan rasm xabarini o'chirish
    if 'last_photo_id' in context.user_data:
        try:
            await context.bot.delete_message(chat_id=query.from_user.id, message_id=context.user_data['last_photo_id'])
            del context.user_data['last_photo_id']
        except Exception as e:
            logger.error(f"Rasmni o'chirishda xatolik: {e}")

    # So'nggi yuborilgan matn xabarini o'chirish
    if 'last_text_id' in context.user_data:
        try:
            await context.bot.delete_message(chat_id=query.from_user.id, message_id=context.user_data['last_text_id'])
            del context.user_data['last_text_id']
        except Exception as e:
            logger.error(f"Matnni o'chirishda xatolik: {e}")

    # So'nggi yuborilgan umumiy xabarni o'chirish (agar mavjud bo'lsa)
    if 'last_message_id' in context.user_data:
        try:
            await context.bot.delete_message(chat_id=query.from_user.id,
                                             message_id=context.user_data['last_message_id'])
            del context.user_data['last_message_id']
        except Exception as e:
            logger.error(f"Umumiy xabarni o'chirishda xatolik: {e}")

    parts = query.data.split('_')  # ['back','to','category','suyuq']
    if len(parts) < 4:
        await query.edit_message_text("Noma'lum orqaga harakat.")
        return
    cat = parts[3]
    await show_dish_categories_logic(cat, query, context)


# ========================= RECIPES BUTTON HANDLER ===========================
async def recipes_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_main_taomlar_menu(update, context)


# =========================== ASOSIY BOT (MAIN) =========================
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # /start komandasi
    application.add_handler(CommandHandler("start", start))

    # Til tanlash callback
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^lang_(uz|ru|en)$'))

    # Foydalanuvchi ma'lumotlarini qabul qilish (TEXT)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_data))

    # Maqsad tanlash: goal_gain, goal_lose, goal_maintain
    application.add_handler(CallbackQueryHandler(goal_selection, pattern='^goal_(gain|lose|maintain)$'))

    # "Taomlar retsepti" => 'recipes'
    application.add_handler(CallbackQueryHandler(recipes_button_handler, pattern='^recipes$'))

    # Bo‘limga kirish: cat_suyuq, cat_quyuq, ...
    application.add_handler(CallbackQueryHandler(show_dish_categories, pattern='^cat_'))

    # Retsept callback: dish_..., drink_..., tort_..., non_, drezden_...
    application.add_handler(CallbackQueryHandler(show_recipe_callback, pattern='^(dish_|drink_|tort_|non_|drezden_).*'))

    # Ortga "taomlar" menu
    application.add_handler(CallbackQueryHandler(back_to_taomlar, pattern='^back_to_taomlar$'))

    # Ortga kategoriya
    application.add_handler(CallbackQueryHandler(back_to_category_handler, pattern='^back_to_category_.*$'))

    # Botni ishga tushiramiz
    application.run_polling()


if __name__ == '__main__':
    main()

