# 교사X 11화 그림 프롬프트 생성기 — 실행: python3 ep11_prompts.py > req_img.json
import json,sys
E=dict(D='ea997844-73ab-4258-8dd0-8940d0076093',VP='e314203d-6f17-44da-a6c3-0638abbbf0af',CA='470494c7-6fbe-412e-aaa5-33c7a8ae77c0',
 CH='bf7aa7d0-ac76-4b27-9022-01373b87ba93',CHO='31a0d225-f8ae-4d63-adba-95cf0df2dd4a',COR='f646c2c7-45e5-40be-8427-d764ce0dd422',
 OF='98bebb3b-ef33-4f76-b103-30a0731898d1',CL='b8369b1c-c53e-4501-b9fb-08a085cb794c',PEN='2af71b8d-318f-4a5a-8bc7-6687caab18aa',
 W='f4311bd5-c6a7-405b-8563-6b99d83e7151',RP='ba71d505-448d-4ea9-8554-f0dff0a0d4e9',JH='5a303a9c-e741-43ae-bb1e-c024ba6cce00',EN='34f6597e-9be2-47a2-96d2-0ba6ba6db13a')
def e(k): return '<<<%s>>>'%E[k]
DH=f"{e('D')} in a black suit and white blouse, red fountain pen {e('PEN')} clipped in her breast pocket, silver watch {e('W')}, flat expressionless face, no smile,"
CHR=f"{e('CH')} the elderly chairman in a dark brown suit, red fountain pen {e('PEN')} in his breast pocket,"
ENV=f"the cream envelope with a red seal {e('EN')}"
VPP=f"{e('VP')} in a dark grey suit with a red necktie and glasses,"
RPP=f"{e('RP')} the reporter with a small black notebook,"
JHP=f"{e('JH')} the student,"
CLS=f"{e('CL')} during 2nd period, bright late-morning daylight through the windows, students in dark green blazers at desks"
CORR=f"the school corridor {e('COR')} in bright late-morning daylight, a classroom door with a glass window on one side"
OFF=f"the staff office {e('OF')} in bright late-morning daylight"
S=[
(301,f"{CHR} holding {ENV}, standing at the open sliding door of {OFF}","he leans in and asks politely, mouth open mid-word, eyebrows raised","medium shot from inside the office, slightly low"),
(302,f"{e('CA')} seated at her desk in {OFF}","she turns her chair toward the door and answers calmly but firmly, mouth open mid-word, one hand raised palm out","medium shot, chairman's shoulder soft in the foreground"),
(303,f"{CHR} holding {ENV} at the door of {OFF}","close-up, he blinks in disbelief and asks back, mouth open, pointing at himself with the envelope","close-up, eye level"),
(304,f"{e('CA')} at her desk in {OFF}","close-up, she nods once with a polite small smile and answers, mouth open mid-word","close-up, slight high angle"),
(305,f"{CHR} walking slowly down {CORR}, {ENV} in his hand","he walks toward the classroom door window, mouth closed","wide shot from behind, long corridor perspective"),
(306,f"{VPP} seated at his desk in {OFF}, holding a desk phone receiver to his ear","he listens with a pained sweating face, lips pressed closed, eyes darting","medium close-up"),
(307,f"{VPP} seated at his desk in {OFF}, holding a desk phone receiver to his ear","he stammers into the phone, mouth open mid-word, free hand waving helplessly","close-up, slight low angle"),
(308,f"{RPP} standing beside the vice principal's desk in {OFF}","she asks briskly, mouth open mid-word, notebook open, pen ready","medium shot over the vice principal's shoulder"),
(309,f"{VPP} seated at his desk in {OFF}, a phone receiver just put down","he answers awkwardly, mouth open mid-word, forced smile","medium close-up, the reporter's shoulder soft in foreground"),
(310,f"{RPP} in {OFF}","close-up, she is genuinely surprised, eyebrows up, mouth open mid-word","close-up, eye level"),
(311,f"{VPP} seated at his desk in {OFF}","he sighs and lifts one hand in surrender, answering, mouth open mid-word","medium close-up"),
(312,f"{RPP} in {CORR}","she walks up to the classroom door and peers through its glass window, curious, mouth closed","medium shot from the side"),
(313,f"{DH} standing at the blackboard at the front of {CLS}","she holds chalk, having drawn a vertical line splitting the board into two empty columns, she speaks to the class, mouth open mid-word","medium shot from a student's seat, students' backs in foreground"),
(314,f"{DH} at the teacher's desk at the front of {CLS}, an open attendance book in her hand","she looks up from the book toward one empty seat and calls a name, mouth open mid-word","medium close-up, slight low angle"),
(315,f"{CLS}, one empty desk with a backpack hanging on it","students seen from behind turn to each other and whisper, shrugging","wide shot from the back of the classroom"),
(316,f"a plain round white wall clock with black hands and no numbers above the blackboard of {CLS}","insert","extreme close-up"),
(317,f"{JHP} at the sliding door at the back of {CLS}","he slides the door open and strolls in casually, one hand in pocket, mouth closed","medium shot from inside the classroom"),
(318,f"{DH} at the front of {CLS}","she looks straight at the late student, flat face, mouth open mid-word","medium close-up over the student's shoulder in foreground"),
(319,f"{JHP} standing just inside the back door of {CLS}","he answers carelessly with a half smirk, mouth open mid-word, scratching his neck","medium close-up"),
(320,f"{DH} in {CLS}","close-up, calm and firm, she speaks, mouth open mid-word","close-up, low angle, window light on her face"),
(321,f"{JHP} standing beside his desk in {CLS}","close-up, defiant frown, he talks back, mouth open mid-word","close-up, eye level"),
(322,f"{DH} at the blackboard of {CLS}","she taps the chalk on the board beside two large written characters, turning to face the student, mouth open mid-word","medium shot, the board characters blurred and out of focus"),
(323,f"{DH} standing near the student's desk in {CLS}","close-up, she speaks quietly and calmly, slight lean forward, mouth open mid-word, not angry","close-up, eye level, soft window light"),
(324,f"{JHP} seated at his desk in {CLS}","close-up, stunned speechless, eyes wide, lips closed","close-up, slight high angle"),
(325,f"{CHR} holding {ENV} and {RPP} standing side by side in {CORR}","they look through the glass window of the classroom door, both mouths closed, the chairman's grip on the envelope loosens, the reporter writes in her notebook","medium shot from inside the classroom looking out through the door window"),
(326,f"{DH} stepping out of the classroom door into {CORR}, facing {CHR}","she speaks to him politely, mouth open mid-word","medium shot over the chairman's shoulder"),
(327,f"{CHR} in {CORR}","he hides {ENV} behind his back, flustered fake smile, mouth open mid-word","medium close-up"),
(328,f"{VPP} hurrying up in {CORR}","he speaks breathlessly, mouth open mid-word, one hand raised","medium shot"),
(329,f"{DH} in {CORR}","close-up, flat face, she speaks evenly, mouth open mid-word","close-up, eye level"),
(330,f"{RPP} in {CORR}","she steps forward holding out her notebook and asks, mouth open mid-word","medium close-up"),
(331,f"{DH} in {CORR}","she answers the reporter firmly, mouth open mid-word, chin up","low angle medium close-up, window light behind her"),
(332,f"{CHR} seated at his desk in {e('CHO')} in the evening","he slides {ENV} into the open desk drawer, mouth closed","medium shot, desk lamp light"),
(333,f"close-up of {e('D')}'s fingers turning the cap of the red fountain pen {e('PEN')}, silver watch {e('W')} on her wrist, at a desk in {OFF} in the evening","insert","extreme close-up"),
(334,f"{DH} sitting at a desk in {OFF} in the evening, looking out the window","close-up, quiet thoughtful face, lips closed","close-up, evening window light"),
]
STY="Korean webtoon style illustration, clean ink line art, soft cel shading, muted realistic colors."
R=[]
for i,s,a,c in S:
    R.append({"index":i,"params":{"model":"gpt_image_2_6","quality":"high","resolution":"2k","aspect_ratio":"9:16",
     "prompt":f"{STY} SUBJECT: {s}. ACTION: {a}. CAMERA: {c}, no one looks at the camera. No text, no letters, no numbers on any paper, screen, board or sign."}})
json.dump({"requests":R},sys.stdout,ensure_ascii=False,indent=0)
