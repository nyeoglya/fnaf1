from audiomanager import AudioManager

baseWidth, baseHeight = 1280, 720 # 1080, 720도 가능함
titleMainAudio = AudioManager('./resources/audio/title_main.wav', repeated=True)
titleStaticAudio = AudioManager('./resources/audio/title_static.wav', repeated=True)
titleStaticAudio.set_volume(0.5)

officeMainAudio = AudioManager('./resources/audio/office_main.wav', repeated=True)
officeFanAudio = AudioManager('./resources/audio/office_fan.wav', repeated=True)
officeFanAudio.set_volume(0.4)
officeLightAudio = AudioManager('./resources/audio/office_light.wav', repeated=True)
officeDoorAudio = AudioManager('./resources/audio/office_door.wav', repeated=False)
officeKnockAudio = AudioManager('./resources/audio/office_knock.wav', repeated=False)

cameraMainAudio = AudioManager('./resources/audio/camera_main.wav', repeated=True)
cameraOpenAudio = AudioManager('./resources/audio/camera_open.wav', repeated=False)
cameraCloseAudio = AudioManager('./resources/audio/camera_close.wav', repeated=False)
cameraBlipAudio = AudioManager('./resources/audio/camera_blip.wav', repeated=False)
cameraErrorAudio = AudioManager('./resources/audio/camera_error.wav', repeated=False)
cameraKitchenAudio = AudioManager('./resources/audio/camera_kitchen.wav', repeated=True)
cameraKitchenMoveAudio = AudioManager('./resources/audio/camera_kitchen_move.wav', repeated=True)

hoxyRunAudio = AudioManager('./resources/audio/hoxy_run.wav', repeated=False)
hoxyKnockAudio = AudioManager('./resources/audio/hoxy_knock.wav', repeated=False)

winMainAudio = AudioManager('./resources/audio/win_main.wav', repeated=False)
winYayAudio = AudioManager('./resources/audio/win_yay.wav', repeated=False)
powerDownAudio = AudioManager('./resources/audio/powerdown.wav', repeated=False)
screamAudio = AudioManager('./resources/audio/scream.wav', repeated=False)
musicBoxAudio = AudioManager('./resources/audio/musicbox.wav', repeated=False)
