# 교사X 11화 반응 영상(kling3_0 std, 소리 끔, 4초) 요청 생성기 — 요소 <<<ID>>> 포함(매뉴얼 5절)
import json,sys
E=dict(D='ea997844-73ab-4258-8dd0-8940d0076093',VP='e314203d-6f17-44da-a6c3-0638abbbf0af',CH='bf7aa7d0-ac76-4b27-9022-01373b87ba93',
 CHO='31a0d225-f8ae-4d63-adba-95cf0df2dd4a',COR='f646c2c7-45e5-40be-8427-d764ce0dd422',OF='98bebb3b-ef33-4f76-b103-30a0731898d1',
 CL='b8369b1c-c53e-4501-b9fb-08a085cb794c',PEN='2af71b8d-318f-4a5a-8bc7-6687caab18aa',W='f4311bd5-c6a7-405b-8563-6b99d83e7151',
 RP='ba71d505-448d-4ea9-8554-f0dff0a0d4e9',JH='5a303a9c-e741-43ae-bb1e-c024ba6cce00',EN='34f6597e-9be2-47a2-96d2-0ba6ba6db13a')
def e(k): return '<<<%s>>>'%E[k]
IMG={305:'55847f6f-cd21-4dc1-9dbf-4a2b15fd8e09',306:'d902fa35-d35c-4fe6-8010-b2d1aa051ffa',312:'d99d833a-582d-40cb-bc15-ce045d8f61ce',313:'2d6fbb9e-6709-4190-ae9e-ce3d1f1717aa',
 315:'02b060fe-0f7e-4ee9-8c7e-5195d1227245',3161:'bf683ced-c446-416f-ae69-f9f4bae80989',317:'cf7abf7e-9e3b-469f-8eb3-72d250f0f44f',324:'42d40052-93f5-46a8-aedc-994bcf18f375',
 325:'af7344ce-afac-45c4-a3c0-062f720cc3de',332:'81e66bc8-649f-4410-9721-3a2223709703',333:'914842b8-d393-496b-a5a4-6b7507485dd2',334:'PENDING334'}
K=[
(305,f"{e('CH')} walks slowly down the corridor {e('COR')} holding the envelope {e('EN')}, toward the classroom door window. Mouth closed.","slow follow from behind"),
(306,f"{e('VP')} in the staff office {e('OF')} holds the phone receiver to his ear, listening, wincing, wipes sweat from his forehead with his free hand. Lips pressed closed.","static"),
(312,f"{e('RP')} walks up to the classroom door in the corridor {e('COR')} and leans in to peer through the glass window, eyebrows rising. Mouth closed.","slow push in"),
(313,f"{e('D')} at the blackboard in the classroom {e('CL')} draws one vertical chalk line down the middle of the board, then turns to the class. Mouth closed. Students' backs in foreground.","static"),
(315,"Students seen from behind turn to each other, shrug and whisper, one points at an empty desk. Faces mostly hidden.","static"),
(3161,"The minute hand of the wall clock sweeps forward quickly, a quarter turn, time passing.","static, no camera move"),
(317,f"{e('JH')} slides the back door of the classroom {e('CL')} open and strolls in casually, one hand in his pocket. Mouth closed.","static"),
(324,f"{e('JH')} at his desk in the classroom {e('CL')} stares, stunned, blinks twice, then slowly lowers his eyes and sits still. Lips closed.","very slow push in"),
(325,f"{e('CH')} and {e('RP')} look through the classroom door window from the corridor; the chairman's hand holding the envelope {e('EN')} slowly lowers, the reporter writes quickly in her notebook. Both mouths closed.","static"),
(332,f"{e('CH')} in his office {e('CHO')} slides the envelope {e('EN')} into the desk drawer and slowly closes it. Mouth closed.","slow push in"),
(333,f"Fingers of {e('D')} slowly turn the cap of the red fountain pen {e('PEN')} once, then stop. Silver watch {e('W')} visible.","static macro"),
(334,f"{e('D')} sits by the window in the evening staff office {e('OF')}, quiet, still, then turns her eyes slightly. Lips closed, no smile.","very slow push in"),
]
R=[]
for i,a,c in K:
    R.append({"index":i,"params":{"model":"kling3_0","mode":"std","sound":"off","duration":4,"aspect_ratio":"9:16",
     "prompt":f"Korean webtoon anime look, keep the exact characters, faces, clothes, room and lighting of the start image. No text, no music. No one looks at the camera. {a} Camera: {c}.",
     "medias":[{"value":IMG[i],"role":"start_image"}]}})
json.dump({"requests":R},sys.stdout,ensure_ascii=False)
