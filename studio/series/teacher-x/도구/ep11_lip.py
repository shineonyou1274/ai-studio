# 교사X 11화 대사 영상(minimax_h3_max) 요청 생성기 — python3 ep11_lip.py ids.json > req_lip.json
# ids.json: {"img":{"301":job,...},"au":{"01":[job,dur],...}}
import json,sys,math
ids=json.load(open(sys.argv[1]))
SHEET=dict(D='7cbf684e-6c7a-4c66-b125-aa1e217d9c43',VP='7d5c63b4-3afa-4e9d-8877-5f8439608a37',CA='f875372d-8f11-4edd-a1d5-8b5e1af89301',
 CH='703a8d8a-8b2f-4690-895a-f893fac562cb',RP='28502692-a9bf-49f9-8c32-e6f1f168b366',JH='4bb2cb19-5a5c-461b-8803-ef00cdf69a07',S1=None,S2=None,S3=None)
CHAR=dict(D="the woman teacher from the references (straight black shoulder-length hair, black suit, white blouse, red fountain pen in her breast pocket, silver watch). Calm, cold, expressionless face, no smile.",
 VP="the middle-aged vice principal from the references (dark hair, glasses, dark grey suit, red necktie).",
 CA="the woman teacher from the references (brown hair in a low bun, round glasses, beige cardigan).",
 CH="the chairman from the references (neatly combed-back silver hair, clean-shaven, no beard, charcoal black three-piece suit, navy tie, red fountain pen in his breast pocket).",
 RP="the woman reporter from the references (black chin-length bob, navy blazer, white shirt, lanyard, small black notebook).",
 JH="the high school boy from the references (messy black hair with fringe, dark green school blazer, loose tie).",
 S1="the high school girl with a ponytail in a dark green school blazer.",S2="the high school boy with a buzz cut in a dark green school blazer.",S3="the high school girl with short hair, clips and glasses in a dark green school blazer.")
OFF="school staff office, bright late-morning daylight"; CLS="high school classroom during class, bright late-morning daylight"; COR="school corridor outside a classroom, bright late-morning daylight"
L=[ # line, img, who, scene, action, camera
('01','301','CH',OFF,"he leans in at the sliding door holding the cream envelope and asks politely","Static, slight handheld breathing."),
('02','302','CA',OFF,"she turns to the door and answers calmly but firmly, one hand raised palm out","Static."),
('03','303','CH',OFF,"close-up, he blinks in disbelief and asks back, pointing at himself with the envelope","Slow push in."),
('04','304','CA',OFF,"close-up, she nods once with a polite small smile and answers","Static."),
('06','307','VP',OFF,"he stammers into the desk phone receiver, free hand waving helplessly, sweating","Slight handheld."),
('07','308','RP',OFF,"she asks briskly, notebook open, pen ready","Static over the shoulder."),
('08','309','VP',OFF,"he answers awkwardly with a forced smile","Static."),
('09','310','RP',OFF,"close-up, genuinely surprised, eyebrows up, she asks back slowly","Slow push in."),
('10','311','VP',OFF,"he sighs and lifts one hand in surrender, answering","Static."),
('11','S1img','S1',CLS,"she raises her hand casually and asks","Static."),
('12','S2img','S2',CLS,"he raises his hand lazily and asks","Static."),
('13','S3img','S3',CLS,"she raises her hand politely and asks","Static."),
('14','3131','D',CLS,"she speaks flatly to the class, tapping the chalk once on each side of the line she drew on the board","Very slow push in."),
('16','314','D',CLS,"she looks up from the attendance book toward one empty seat and calls the name","Static."),
('18','318','D',CLS,"arms crossed, she looks straight at the late student and speaks flatly","Static."),
('19','3191','JH',CLS,"he answers carelessly with a half smirk, scratching his neck","Static."),
('20','320','D',CLS,"close-up, calm and firm, she speaks","Slow push in."),
('21','321','JH',CLS,"close-up, defiant frown, he talks back","Static, slight handheld."),
('22','3221','D',CLS,"she speaks slowly and deliberately beside the blackboard, chalk in hand","Slow push in."),
('23','323','D',CLS,"close-up, she leans slightly toward the seated student and speaks quietly and calmly, not angry","Very slow push in."),
('26','326','D',COR,"she has just stepped out of the classroom and speaks politely to the chairman","Static over the shoulder."),
('27','327','CH',COR,"he hides the envelope behind his back with a flustered fake smile, answering","Static."),
('28','328','VP',COR,"he hurries up breathlessly and speaks, one hand raised","Static."),
('29','329','D',COR,"close-up, flat face, she speaks evenly","Static."),
('30','330','RP',COR,"she steps forward holding out her notebook and asks","Static."),
('31','331','D',COR,"low angle, she answers the reporter firmly, chin up","Very slow push in."),
]
R=[]
for ln,im,who,sc,act,cam in L:
    aj,dur=ids['au'][ln]; d=max(5,math.ceil(dur+0.4)); img=ids['img'][im]
    med=[{"value":img,"role":"image_references"}]
    sh=SHEET.get(who)
    if sh: med.append({"value":sh,"role":"image_references"})
    med.append({"value":aj,"role":"audio_references"})
    p=(f"GLOBAL STYLE: Korean webtoon anime look, clean line art, flat cel shading. No text, no music.\n"
       f"SCENE: exactly the scene in the first reference image: {sc}.\n"
       f"CHARACTERS: {CHAR[who]} Keep the face exactly as in the first reference image. The only one speaking.\n"
       f"SHOT: same framing as the first reference image. 0-{dur:.1f}s {act}, speaking the reference audio. Then lips pressed together, mouth closed, small natural breathing.\n"
       f"CAMERA: {cam} No one looks at the camera.\n"
       f"AUDIO: lip-sync to the reference audio, lips move with every syllable; after the last word lips pressed together, mouth closed.")
    R.append({"index":int(ln),"params":{"model":"minimax_h3_max","resolution":"480p","duration":d,"aspect_ratio":"9:16","prompt":p,"medias":med}})
json.dump({"requests":R},sys.stdout,ensure_ascii=False)
sys.stderr.write('total sec %d\n'%sum(r['params']['duration'] for r in R))
