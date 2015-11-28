__author__ = 'Anirudh'

import nltk
nltk.data.path.append("/home/anirudhn/nltk_data")
from nltk.corpus import stopwords
from nltk.tag import StanfordNERTagger

st = StanfordNERTagger('stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz','stanford-ner-2014-06-16/stanford-ner.jar',encoding='utf-8')


'''Location, Person, Organization, Money, Percent, Date, Time'''


def named_entity_recognition(stopwords_free_sentences_list):

    NER_list=[]

    person_list=[]
    org_list=[]
    loc_list=[]
    month_list=[]
    time_list=[]
    money_list=[]
    percent_list=[]
    profession_name_list=[]
    temp_list=[]


    time=['yesterday','today','tomorrow','weekend','an hour ago','in an hour','time',
          'recently','soon','age','ago','old','a little while ago','at this moment','in the near future','a long time ago','these days',
          'those days','way off in the future','in the past','nowadays','eventually','this morning','at this time',
          'later this evening','morning', 'evening','night','midnight','dawn','dusk','afternoon','noon','midday',
          'am','pm','sunrise','sunset','lunchtime','teatime','dinnertime','interval','twilight','beginning',
          'hourly','nightly','daily','monthly','weekly','quarterly','yearly',
          'fall','winter','equinox','solstice',
          'january','february','march','april','may','june','july','august','september','october','november','december',
          'years','year', 'month','months', 'day','days', 'week','weeks', 'hour','hours', 'minute','minutes', 'second','seconds',
          'fortnight','halfhour','quarter','quarter hour','half']


    profession=['actor','actress','hero','heroine','villain','accountant','agronomist','animator','anthropologist','archaeologist','architect',
                'artist','astrologer','astronomer','athlete','auctioneer','auditor',
                'baker','banker','barber','beautician','biologist','biochemist','botanist','butler',
                'caretaker','carpenter','cartographer','chemist','choreographer','cleaner','clerk','composer','commentator','reporter','journalist',
                'conductor','cook','dancer','diver','dresser','driller','doctor','director',
                'editor','economist','electrician','engineer',
                'farmer','firefighter','fisherman','geographer','geologist','gardener','goldsmith','historian','lawyer',
                'manager','miner','minister','metrologist','meteorologist','musician',
                'nurse','officer','packer','pawnbroker','pharmacist','philosopher','photographer','police',
                'principal','producer','psychologist','psychiatrist','registrar','referee',
                'singer','songwriter','statistician','stockbroker','tailor','teller','tutor',
                'husband','administrative services department manager','agricultural advisor','air-conditioning installer','mechanic',
'aircraft service technician','ambulance driver','animal carer','arable farm manager','arable farmer','architect',
'asbestos removal worker','assembler','leader','assembly team leader','team leader','bank clerk','beauty therapist',
'beverage production process controller','boring machine operator','bricklayer','butcher','car mechanic','charge nurse',
'check-out operator','child care services manager','baby care taker','child-carer','civil engineering technician','cleaning supervisor',
'climatologist','cloak room attendant','cnc operator','community health worker','company director','confectionery maker',
'construction operative','cooling or freezing installer','database designer','dental hygienist','dentist','dental prosthesis technician',
'department store manager','dietician','display designer','domestic housekeeper','education advisor','electrical engineer',
'electrical mechanic or fitter','engineering maintenance supervisor','estate agent','executive secretary','felt roofer','filing clerk',
'financial clerk','financial services manager','fire fighter','first line supervisor beverages workers',
'first line supervisor of cleaning workers','flight attendant','floral arranger','food scientist','garage supervisor','gardener',
'general practitioner','hairdresser','head groundsman','horse riding instructor','hospital nurse','hotel manager','house painter',
'hr manager','it applications programmer','it systems administrator','journalist','judge','kitchen assistant','lathe setter-operator',
'legal secretary','legal expert','local police officer','logistics manager','machine tool operator','health services manager',
'meat processing operator','mechanical engineering technician','medical laboratory technician','medical radiography equipment operator',
'metal moulder','metal production process operator','meteorologist','midwifery professional','mortgage clerk','musical instrument maker',
'non-commissioned officer armed forces','nursery school teacher','nursing aid','ophthalmic optician','payroll clerk',
'personal carer in an institution for the elderly','personal carer in an institution for the handicapped',
'personal carer in private homes','personnel clerk','pest controller','physician assistant','pipe fitter','plant maintenance mechanic',
'plumber','police inspector','policy advisor','post secondary education teacher','post sorting or distributing clerk',
'power plant operator','primary school head','primary school teacher','printing machine operator','psychologist',
'quality inspector','receptionist','restaurant cook','road paviour','roofer','sailor','sales assistant','sales or marketing manager',
'sales representative','president','federation','sales support clerk','seaman','secondary school manager','secondary school teacher','secretary','security guard',
 'sheet metal worker','ship mechanic','shoe repairer','leather repairer','social photographer','soldier','speech therapist','steel fixer',
 'stockman','structural engineer','surgeon','surgical footwear maker','swimming instructor','tailor','seamstress','tax inspector',
 'taxi driver','tile layer','transport clerk','travel agency clerk','truck driver long distances','university professor',
 'university researcher','veterinary practitioner','vocational education teacher','waiting staff','web developer','welder',
 'wood processing plant operator','volunteer']



    #for i in range(0, len(stopwords_free_sentences_list)):
    NER_list = st.tag(stopwords_free_sentences_list.split())

    #print 'NER List:', NER_list

    for i in range(0,len(NER_list)):
        #print NER_list[i][0].lower()
        if NER_list[i][1]=='PERSON':
            #print 'Person true'
            person_list.append(NER_list[i][0])
        elif NER_list[i][1]=='ORGANIZATION':
            org_list.append(NER_list[i][0])
        elif NER_list[i][1]=='LOCATION':
            loc_list.append(NER_list[i][0])
        elif NER_list[i][1]=='DATE':               #Month and weekday names
            month_list.append(NER_list[i][0])
        elif NER_list[i][1]=='TIME' or NER_list[i][0].lower() in time:
            time_list.append(NER_list[i][0])
        elif NER_list[i][1]=='MONEY':
            money_list.append(NER_list[i][0])
        elif NER_list[i][1]=='PERCENT':
            percent_list.append(NER_list[i][0])
        elif NER_list[i][0].lower() in profession:       #Profession name list
            profession_name_list.append(NER_list[i][0])



    return person_list,org_list,loc_list,month_list,time_list,money_list,percent_list,profession_name_list

