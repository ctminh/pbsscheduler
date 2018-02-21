import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def plotAVEWaitingTime():
    objects = ('SJF-BF', 'LJF-BF', 'FCFS-BF', 'H', 'ML')
    y_pos = np.arange(len(objects))
    performance = [1799.99, 13882.255, 3528.55, 100, 100]

    plt.bar(y_pos, performance, align='center', alpha=0.4)
    plt.xticks(y_pos, objects)
    plt.ylabel('Average Waiting Time (s)')
    plt.title('Scheduling Policies')
    # plt.legend()
    plt.grid()
    plt.savefig('graphs/AVEWaitingTime.png')

    plt.show()

def plotAVETurnAroundTime():
    objects = ('SJF-BF', 'LJF-BF', 'FCFS-BF', 'H', 'ML')
    y_pos = np.arange(len(objects))
    performance = [1990.935, 14064.015, 3697.485, 100, 100]

    plt.bar(y_pos, performance, align='center', alpha=0.4, color='olive')
    plt.xticks(y_pos, objects)
    plt.ylabel('Average TurnAround Time (s)')
    plt.title('Scheduling Policies')
    # plt.legend()
    plt.grid()
    plt.savefig('graphs/AVETurnAroundTime.png')

    plt.show()

def plotThroughput():
    objects = ('SJF-BF', 'LJF-BF', 'FCFS-BF', 'H', 'ML')
    y_pos = np.arange(len(objects))
    performance = [41.61, 44.055, 50.89, 1, 1]
    error = np.random.rand(len(objects))

    plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
    plt.yticks(y_pos, objects)
    plt.xlabel('Thoughput (#jobs/hour)')
    # plt.ylabel('Scheduling Policies')
    plt.grid()
    plt.savefig('graphs/AVEThroughput.png')

    plt.show()

def plotAVEbsld():
    objects = ('SJF-BF', 'LJF-BF', 'FCFS-BF', 'H', 'ML')
    y_pos = np.arange(len(objects))
    performance = [14.486, 811.67, 138.637, 0, 0]

    plt.bar(y_pos, performance, align='center', alpha=0.4, color='navy')
    plt.xticks(y_pos, objects)
    plt.ylabel('Average Bounded Slowdown (s)')
    plt.title('Scheduling Policies')
    # plt.legend()
    plt.grid()
    plt.savefig('graphs/AVEbsld.png')

    plt.show()

if __name__ == '__main__':
    plotAVEWaitingTime()
    # plotAVETurnAroundTime()
    # plotThroughput()
    # plotAVEbsld()