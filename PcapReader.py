from netzob.all import *
import copy

def ImportMessage():
    """
    将报文包导入,并输出原始报文包以及用-1补齐后的报文包
    :return: 原始报文包,用-1补齐后的报文包
    """
    message_session1 = PCAPImporter.readFile('ftp1.pcap').values()
    message_session2 = PCAPImporter.readFile('ftp2.pcap').values()
    message_session3 = PCAPImporter.readFile('ftp3.pcap').values()
    message_session4 = PCAPImporter.readFile('ftp4.pcap').values()
    message = message_session1 + message_session2 + message_session3 + message_session4
    symbol = Symbol(messages=message)

    #将pcap包中的内容转换为二维列表
    message_list_original = symbol.getValues()

    message_list_tmp = copy.deepcopy(message_list_original)
    for i in range(len(message_list_tmp)):
        if b'\r' in message_list_tmp[i]:
            message_list_tmp[i] = message_list_tmp[i].replace(b'\r',b'')
        if b'\n' in message_list_tmp[i]:
            message_list_tmp[i] = message_list_tmp[i].replace(b'\n',b'')
        if b'\r\n' in message_list_tmp[i]:
            message_list_tmp[i] = message_list_tmp[i].replace(b'\r\n',b'')
        if b'\t' in message_list_tmp[i]:
            message_list_tmp[i] = message_list_tmp[i].replace(b'\t',b'')
    message_list_tmp,message_list_original = message_list_original,message_list_tmp

    message_list = []
    for i in range(len(message_list_tmp)):
        message_list.append(list(message_list_tmp[i]))

    #计算报文的最大长度
    message_max_lenth = 0
    for i in range(len(message_list)):
        if len(message_list[i]) > message_max_lenth:
            message_max_lenth = len(message_list[i])

    #用-1补齐报文
    for i in range(len(message_list)):
        message_lenth = len(message_list[i])
        for j in range(message_lenth,message_max_lenth):
            message_list[i].append(-1)

    return message_list_original,message_list

if __name__ == '__main__':
    message_list_original,message_list = ImportMessage()
    print('original message is:')
    for i in range(len(message_list_original)):
        print(message_list_original[i])

    print("\n\n\n")

    print('message_list is:')
    for i in range(len(message_list)):
        print(message_list[i])