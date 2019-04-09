import os
import time
import traceback
from multiprocessing import Queue,Process,Manager
from queue import Empty,Full

def paralleled(num, pqueue,log_queue,ret_queue):
    while 1:# pqueue.empty():
        print(f'进程{num}提取数据')
        try:
            type,data = pqueue.get(block=True, timeout=0.01)
        except Empty:
            time.sleep(0.1)
            continue
        print(f'进程{num}生成中间结果')

        if type == 'control':
            print('exit ',num,os.getpid())
            break

        """ Save data to database """
        try:
                #security_value_df.to_sql('ESGX_SECURITY_VALUE_RESEARCH', db_connect, if_exists='append', index=False) #, schema=port_cfg['client_schema'])
            #c = Utils.ora_connector(pool=0)
            #a = pd_to_db.df_to_db(c)
            if 1:
                #a.insert_many('ESGX_SECURITY_VALUE_RESEARCH',security_value_df)
                log_queue.put('out%d' % num,timeout=0.01)
                ret_queue.put('out%d' % num,timeout=0.01)
                #security_value_df.to_csv('Result_ESGX_SECURITY_VALUE.csv', mode='a',encoding='utf8')  # , schema=port_cfg['client_schema'])
        except Full:
            traceback.print_exc()
        print(f'进程{num}结束')
        time.sleep(0.1)

def calculate_daily_port_values():
    pqueue, log_queue, ret_queue = Queue(20), Queue(5), Queue(5)
    mgr = Manager()
    ns = mgr.list()
    for dt_current_index in range(8):
        pqueue.put(['data','test%d' % dt_current_index])

    for dt_current_index in range(8):
        pqueue.put(['control','exit'])

    cpus = 8
    p = []
    print('---------------------------------Start to Parallel')
    for i in range(cpus):
        p.append(Process(target=paralleled, args=(i, pqueue, log_queue, ret_queue)))
    print(f'多进程数量为{len(p)}')
    for i in p:
        i.start()
    for i in p:
        i.join()
        print('end join',i.ident)
    print('Join_Finished')

def main():
    calculate_daily_port_values()

if __name__ == '__main__':
    main()