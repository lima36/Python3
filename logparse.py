import re

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
timestamp = r'\[(\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\]'
regex = r'\[(\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\] <(\w*)> \[(.*)\](.*)'
action = r'\[(\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\] <(\w*)> \[(ExtInterfaceService)\]( Current Action Status .*)'
mcu_info = r'\[(\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\] <(\w*)> \[(w_)\],(.*)'
position = r'\[(\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\] <(\w*)> \[(slam_)\],(.*)'
mov2goal = r'\[(\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\] <(\w*)> \[(ExtInterfaceService)\] Action Msg \[ ID\(.*\)'
robot_state = r'\[(\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\] <(\w*)> \[(navicore::component::ActionState_)'
booting = r'\[(\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6})\] <(\w*)> \[mmedia_\] load micom\.yml.*'
elevator = r'elevator'
#robot.yml
#[SLAMSrv] OnInialize
#[LocalMapSrv] OnStart
#[VisualLocalization] OnInitialize
#

def filterInLogfile(filePath, regStr):
    pActionStatus = None
    pMCU = None
    pPosition = None
    searchlist = []
    with open(filePath, 'r') as logFile:
        for line in logFile:
            line = ansi_escape.sub('', line)
            matchobj = re.search(regStr, line)
            if matchobj is not None:
                iActionStatus = re.search(action, line)
                iMCUinfo = re.search(mcu_info, line)
                iPosition = re.search(position, line)

                if iActionStatus is not None:
                    if iActionStatus.group(4) != pActionStatus:
                        # print(line)
                        searchlist.append(line)
                    pActionStatus = iActionStatus.group(4)
                elif iMCUinfo is not None:
                    mcu_infos = iMCUinfo.group(4).split(",")
                    if pMCU is None:
                        # print(line)
                        searchlist.append(line)
                    else:
                        for n in [1, 2, 3, 4, 6, 7, 8, 9, 10]:
                            if mcu_infos[n] != pMCU[n]:
                                # print(line)
                                searchlist.append(line)
                                break
                    pMCU = iMCUinfo.group(4)
                    #[12-24 00:31:30.987836] <info> [slam_],77127, 1608737490987, 1608737490987, 1608737490985,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000,-1.09827,1.84947,34.96107,14.73820,13.47135,2.00000,-169.39865,14.66150,13.83215,2.00000,-175.06322,0,0,0,
                elif iPosition is not None:
                    position_info = iPosition.group(4).split(",")
                    if pPosition is None:
                        # print(line)
                        searchlist.append(line)
                    else:
                        for n, item in enumerate(position_info):
                            if n <5: continue
                            else:
                                if item == pPosition[n]:
                                    searchlist.append(line)
                                    break
                        pPosition = iPosition.group(4)

    return searchlist


def filterInList(logList, regStr):
    pActionStatus = None
    pMCU = None
    pPosition = None
    searchlist = []

    for line in logList:
        line = ansi_escape.sub('', line)
        matchobj = re.search(regStr, line)
        if matchobj is not None:
            iActionStatus = re.search(action, line)
            iMCUinfo = re.search(mcu_info, line)
            iPosition = re.search(position, line)

            if iActionStatus is not None:
                if iActionStatus.group(4) != pActionStatus:
                    # print(line)
                    searchlist.append(line)
                pActionStatus = iActionStatus.group(4)
            elif iMCUinfo is not None:
                mcu_infos = iMCUinfo.group(4).split(",")
                if pMCU is None:
                    # print(line)
                    searchlist.append(line)
                else:
                    for n in [1, 2, 3, 4, 6, 7, 8, 9, 10]:
                        if mcu_infos[n] != pMCU[n]:
                            print(line)
                            searchlist.append(line)
                            break
                pMCU = iMCUinfo.group(4)
                #[12-24 00:31:30.987836] <info> [slam_],77127, 1608737490987, 1608737490987, 1608737490985,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000,-1.09827,1.84947,34.96107,14.73820,13.47135,2.00000,-169.39865,14.66150,13.83215,2.00000,-175.06322,0,0,0,
            elif iPosition is not None:
                position_info = iPosition.group(4).split(",")
                if pPosition is None:
                    # print(line)
                    searchlist.append(line)
                else:
                    for n, item in enumerate(position_info):
                        if n < 5: continue
                        else:
                            if item != (pPosition.split(",")[n]):
                                searchlist.append(line)
                                break
                pPosition = iPosition.group(4)

    return searchlist


#[12-24 18:34:49.346099] <info> [ExtInterfaceService] Action Msg [ ID(eMove2Goal) / Node[0](14.9421, 13.8569, 2) / Node[size-1](23.7383, 14.3401, 2) / MaxVel(0)
def find_move2goal(line):
    matchobj = re.search(r".* Node\[0\]\(([0-9.]+, [0-9.]+, [0-9.]+)\) / Node\[size-1\]\(([0-9.]+, [0-9.]+, [0-9.]+)\) .*", line)
    if matchobj is not None:
        pass#print(matchobj.group(1), matchobj.group(2))

def count_booting(inFile):

    pass


def analysis_robot(inFile):
    print("analysis_robot:"+inFile)
    info = []
    with open(inFile, 'r') as logFile:
        prevlog = "analysis_robot"
        for line in logFile:
            line = ansi_escape.sub('', line)
            # matchobj = re.search(mov2goal, line)
            # print(line)
            if re.search(mov2goal, line) is not None:
                find_move2goal(line)
                print(line)
                info.append(line)
            elif re.search(robot_state, line) is not None:
                print(line)
                if "ActionState_Run] Info - RemainDistM" in prevlog:
                    prevlog = line
                    continue
                prevlog = line
                info.append(line)
            elif re.search(booting, line) is not None:
                print(line)
                info.append(line)
    return info


def analysis_elevator(inFile):
    info = []
    with open(inFile, 'r') as logFile:
        word = ["eSTATUS_PATH_FAIL_TARGET_BLOCKED", "offsetResult", "eOutOfElevator", "eInToElevator", "final height(weighted)"]
        for line in logFile:
            line = ansi_escape.sub('', line)
            if re.search("Elevator|EIN|TM|Action Msg", line) is not None:
                if any(s in line for s in word):
                    info.append(line)


    return info

def analysis_elevator2(inFile):
    info = []
    with open(inFile, 'r') as logFile:
        for line in logFile:
            line = ansi_escape.sub('', line)
            if re.search("elevator", line) is not None:
                # print(line)
                info.append(line)
    return info