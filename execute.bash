# ER
nohup python3 main.py 2 2 0.55 0.65 20 1000 7 0 1 > ex1.txt &
nohup python3 main.py 2 2 0.55 1.0 20 1000 7 0 2 > ex2.txt &
nohup python3 main.py 2 2 0.1 0.5 20 1000 7 0 3 > ex3.txt &

# NS
nohup python3 main.py 2 2 0.55 0.8 20 0 0 50000 4 > ex4.txt &
nohup python3 main.py 2 2 0.55 1.0 20 0 0 50000 5 > ex5.txt &
nohup python3 main.py 2 2 0.1 0.5 20 0 0 50000 6 > ex6.txt &
