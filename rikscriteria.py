import time
import os

# as default, stopcriteria function will try to access job data for two minutes, 
# if it is not possible it will break the while loop so it does not run endlessly.
def stopcriteria(jobname, run = True, sleeptime = 15, Maxchecks = 9):
    n = 0
    LPF_list = []

    while run:
        time.sleep(sleeptime)
        n += 1
        print('CHECK ', n)            
        sta_file = '{}.sta'.format(jobname)

        try:
            status_file = open(sta_file, "r", 0)
            for line in status_file:
                # checking if the job has already completed
                if 'COMPLETED SUCCESSFULLY' in line:
                    print('Job {} has completed successfully'.format(jobname))
                    run = False
                    status_file.close()
                    break

                fields = line.split()
                if len(fields) > 0:
                    if fields[0] == '1':
                        LPFvalue = float(fields[6])
                        if LPFvalue not in LPF_list:
                            LPF_list.append(LPFvalue)
                        if len(LPF_list) > 2 and LPF_list[-1] < LPF_list[-2]:
                            os.system('abaqus terminate job=' + jobname)
                            print('Job {} has converged successully'.format(jobname))
                            print(LPF_list)
                            run = False
                            status_file.close()
                    else:
                        continue
            print(LPF_list)

        except:
            if n >= Maxchecks:
                os.system('abaqus terminate job=' + jobname)
                print('ERROR: job has aborted due to limit of time to start running')
                run = False
            continue
