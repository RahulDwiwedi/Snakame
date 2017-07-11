import cx_Freeze

executables = [cx_Freeze.Executable("Snakame.py")]

cx_Freeze.setup(
    name="Snakame",
    options={"build_exe":{"packages":["pygame"],"include_files":["apple.png","background.png","banana.png","eat.mp3","gameover.wav","pause.mp3","score.dat","snakame.png","snake.png","start.wav"]}},
    description = "its a Snake game.",
    executables = executables
    )
