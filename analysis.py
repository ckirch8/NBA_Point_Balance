import pandas as pd
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

def plot(x, y, x_label, y_label, c, title, savename, tx, ty):
    plt.plot(x, y, 'o', color=c, alpha=0.5, markeredgewidth=0.0)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    m, b = np.polyfit(x, y, 1)
    print(title)
    eq = 'y = ' + str('{:.4f}'.format(m)) + 'x + ' + str('{:.4f}'.format(b))
    print(eq)
    plt.text(tx, ty, eq)
    r = '$R^{2}$ = ' + str('{:.6f}'.format(r_squared(x, y)))
    plt.text(tx, (ty - .01), r)
    plt.plot(x, m*x+b, c='black')
    plt.savefig((savename + '.png'))
    plt.figure()

"""Determine R^2 value"""
def r_squared(x, y):
    corr_mat = np.corrcoef(x, y)
    r2 = (corr_mat[0,1])**2
    return r2

def main(argvs):

    file = argvs[0]
    data = pd.read_csv(file, delimiter=',')

    total_avg = data['pb'].mean()
    print("total average: ", total_avg)
    p_means = data.groupby('playoffs')['pb'].mean()
    print("\nplayoff average", p_means)

    p_box = data.boxplot(column='pb', by='playoffs')
    pBoxFig = p_box.get_figure()
    plt.suptitle('')
    p = plt.gca()
    p.set_title('Point Balance for Playoff Teams vs Non Playoff Teams')
    p.set_xlabel('Playoffs (0: no 1: yes)')
    p.set_ylabel('Point Balace')
    pBoxFig.savefig('playoff_box.png')

    c_means = data.groupby('champions')['pb'].mean()
    print("\nchampionship average", c_means)

    c_box = data.boxplot(column='pb', by='champions')
    cBoxFig = c_box.get_figure()
    plt.suptitle('')
    p = plt.gca()
    p.set_title('Point Balance for Championship Teams vs Non Championship Teams')
    p.set_xlabel('Champions (0: no 1: yes)')
    p.set_ylabel('Point Balace')
    cBoxFig.savefig('champ_box.png')

    plt.figure()
    plot(data['wpct'], data['pb'], 'Win Percentage', 'Point Balance', 'blue', 'Win Pecentage vs Point Balance', 'wpct_pb', 0.1, 0.88)
    print('R^2 = ', r_squared(data['wpct'], data['pb']))
    plot(data['ortg'], data['pb'], 'Offensive Rating', 'Point Balance', 'red', 'Offensive Rating vs Point Balance', 'ortg_pb', 95, 0.88)
    print('R^2 = ', r_squared(data['ortg'], data['pb']))
    plot(data['eFG%'], data['pb'], 'eFG%', 'Point Balance', 'green', 'Effective Field Goal Percentage vs Point Balance', 'efg_pb', 0.44, 0.88)
    print('R^2 = ', r_squared(data['eFG%'], data['pb']))


    team_max = data.loc[data.reset_index().groupby(['team'])['pb'].idxmax()]
    print('\nPoint Balance maximums by team')
    print(team_max)
    print("max average", team_max['pb'].mean())
    team_max.to_csv('team_max.csv', index=False, float_format='%.3f')

    team_min = data.loc[data.reset_index().groupby(['team'])['pb'].idxmin()]
    print('\nPoint Balance minimums by team')
    print(team_min)
    print("min average", team_min['pb'].mean())
    team_min.to_csv('team_min.csv', index=False, float_format='%.3f')



    year_max = data.loc[data.reset_index().groupby(['year'])['pb'].idxmax()]
    print('\nPoint Balance maximums by year')
    print(year_max)
    print("max average", year_max['pb'].mean())
    year_max.to_csv('year_max.csv', index=False, float_format='%.3f')

    year_min = data.loc[data.reset_index().groupby(['year'])['pb'].idxmin()]
    print('\nPoint Balance minimums by year')
    print(year_min)
    print("min average", year_min['pb'].mean())
    year_min.to_csv('year_min.csv', index=False, float_format='%.3f')

    print("\nPoint Balance for each champion")
    champ_pb = data.loc[data.reset_index().groupby(['year'])['champions'].idxmax()]
    print(champ_pb)
    champ_pb.to_csv('cham_pb.csv', index=False, float_format='%.3f')

if __name__ == "__main__":
	main(sys.argv[1:])
