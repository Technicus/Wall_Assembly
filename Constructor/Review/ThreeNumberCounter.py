#!/usr/bin/env python3


start = -9
stop = 10

x = 0
y = 0
z = 0

count = 0

print()
print('start = {}'.format(start))
print('stop = {}'.format(stop))
print()
print('x = {}'.format(x))
print('y = {}'.format(y))
print('z = {}'.format(z))
print()
print('count = {:04d}'.format(count))
print()

with open('../Exports/Info/ThreeNumberCounter.info', 'w') as count_report:
    for x in range(start, stop, 1):
        for y in range(start, stop, 1):
            for z in range(start, stop, 1):
                count = count + 1
                count_report.write('{:04d})'.format(count))
                if x > -1:
                    count_report.write('  {}'.format(x))
                    #print('  {} '.format(x), end = '')
                else:
                    count_report.write(' {}'.format(x))
                    #print(' {} '.format(x), end = '')
                if y > -1:
                    count_report.write('  {}'.format(y))
                    #print('  {} '.format(y), end = '')
                else:
                    count_report.write(' {}'.format(y))
                    #print(' {} '.format(y), end = '')
                if z > -1:
                    count_report.write('  {} '.format(z))
                    #print('  {} '.format(z), end = '')
                else:
                    count_report.write(' {} '.format(z))
                    #print(' {} '.format(z), end = '')
                count_report.write('\n')
                with open('../Exports/Info/combination/{:04d}.info'.format(count), 'w') as count_file:
                    count_file.write('count = {:04d}'.format(count))
                #print()

print('count = {:03d}'.format(count))
print()
