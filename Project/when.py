__author__ = 'Anirudh'

import WM
import NET
import nltk

# The selection of answer is based on the sentence which gets the maximum total score across the four conditions ##

# But generally answers to "when" questions almost always involves a time expression, so sentences that do not contain a time
# expression are only considered in special cases

def answering_when(question,cleansedQuestion,stop_words_free_question,sentence_list,dateline):

    # Declaring globals to be used in this function

    candidate_sent_list=[]
    sent_score_list={}
    final_sent_list=[]

    when_year_verbs=['play','fought'] #'win','lose','victorius']

    when_year=['1400', '1401', '1402', '1403', '1404', '1405', '1406', '1407', '1408', '1409', '1410', '1411', '1412', '1413', '1414', '1415', '1416', '1417', '1418', '1419', '1420', '1421', '1422', '1423', '1424', '1425', '1426', '1427', '1428', '1429', '1430', '1431', '1432', '1433', '1434', '1435', '1436', '1437', '1438', '1439', '1440', '1441', '1442', '1443', '1444', '1445', '1446', '1447', '1448', '1449', '1450', '1451', '1452', '1453', '1454', '1455', '1456', '1457', '1458', '1459', '1460', '1461', '1462', '1463', '1464', '1465', '1466', '1467', '1468', '1469', '1470', '1471', '1472', '1473', '1474', '1475', '1476', '1477', '1478', '1479', '1480', '1481', '1482', '1483', '1484', '1485', '1486', '1487', '1488', '1489', '1490', '1491', '1492', '1493', '1494', '1495', '1496', '1497', '1498', '1499', '1500', '1501', '1502', '1503', '1504', '1505', '1506', '1507', '1508', '1509', '1510', '1511', '1512', '1513', '1514', '1515', '1516', '1517', '1518', '1519', '1520', '1521', '1522', '1523', '1524', '1525', '1526', '1527', '1528', '1529', '1530', '1531', '1532', '1533', '1534', '1535', '1536', '1537', '1538', '1539', '1540', '1541', '1542', '1543', '1544', '1545', '1546', '1547', '1548', '1549', '1550', '1551', '1552', '1553', '1554', '1555', '1556', '1557', '1558', '1559', '1560', '1561', '1562', '1563', '1564', '1565', '1566', '1567', '1568', '1569', '1570', '1571', '1572', '1573', '1574', '1575', '1576', '1577', '1578', '1579', '1580', '1581', '1582', '1583', '1584', '1585', '1586', '1587', '1588', '1589', '1590', '1591', '1592', '1593', '1594', '1595', '1596', '1597', '1598', '1599', '1600', '1601', '1602', '1603', '1604', '1605', '1606', '1607', '1608', '1609', '1610', '1611', '1612', '1613', '1614', '1615', '1616', '1617', '1618', '1619', '1620', '1621', '1622', '1623', '1624', '1625', '1626', '1627', '1628', '1629', '1630', '1631', '1632', '1633', '1634', '1635', '1636', '1637', '1638', '1639', '1640', '1641', '1642', '1643', '1644', '1645', '1646', '1647', '1648', '1649', '1650', '1651', '1652', '1653', '1654', '1655', '1656', '1657', '1658', '1659', '1660', '1661', '1662', '1663', '1664', '1665', '1666', '1667', '1668', '1669', '1670', '1671', '1672', '1673', '1674', '1675', '1676', '1677', '1678', '1679', '1680', '1681', '1682', '1683', '1684', '1685', '1686', '1687', '1688', '1689', '1690', '1691', '1692', '1693', '1694', '1695', '1696', '1697', '1698', '1699', '1700', '1701', '1702', '1703', '1704', '1705', '1706', '1707', '1708', '1709', '1710', '1711', '1712', '1713', '1714', '1715', '1716', '1717', '1718', '1719', '1720', '1721', '1722', '1723', '1724', '1725', '1726', '1727', '1728', '1729', '1730', '1731', '1732', '1733', '1734', '1735', '1736', '1737', '1738', '1739', '1740', '1741', '1742', '1743', '1744', '1745', '1746', '1747', '1748', '1749', '1750', '1751', '1752', '1753', '1754', '1755', '1756', '1757', '1758', '1759', '1760', '1761', '1762', '1763', '1764', '1765', '1766', '1767', '1768', '1769', '1770', '1771', '1772', '1773', '1774', '1775', '1776', '1777', '1778', '1779', '1780', '1781', '1782', '1783', '1784', '1785', '1786', '1787', '1788', '1789', '1790', '1791', '1792', '1793', '1794', '1795', '1796', '1797', '1798', '1799', '1800', '1801', '1802', '1803', '1804', '1805', '1806', '1807', '1808', '1809', '1810', '1811', '1812', '1813', '1814', '1815', '1816', '1817', '1818', '1819', '1820', '1821', '1822', '1823', '1824', '1825', '1826', '1827', '1828', '1829', '1830', '1831', '1832', '1833', '1834', '1835', '1836', '1837', '1838', '1839', '1840', '1841', '1842', '1843', '1844', '1845', '1846', '1847', '1848', '1849', '1850', '1851', '1852', '1853', '1854', '1855', '1856', '1857', '1858', '1859', '1860', '1861', '1862', '1863', '1864', '1865', '1866', '1867', '1868', '1869', '1870', '1871', '1872', '1873', '1874', '1875', '1876', '1877', '1878', '1879', '1880', '1881', '1882', '1883', '1884', '1885', '1886', '1887', '1888', '1889', '1890', '1891', '1892', '1893', '1894', '1895', '1896', '1897', '1898', '1899', '1900', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909', '1910', '1911', '1912', '1913', '1914', '1915', '1916', '1917', '1918', '1919', '1920', '1921', '1922', '1923', '1924', '1925', '1926', '1927', '1928', '1929', '1930', '1931', '1932', '1933', '1934', '1935', '1936', '1937', '1938', '1939', '1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999']

    print 'Question is :',cleansedQuestion


    # 1. Check if the sentence contains "TIME" expression

    for i in range(0,len(sentence_list)):
        score=0
        person_list,org_list,loc_list,time_list,prof_list = NET.named_entity_tagging(sentence_list[i])

        if time_list != []: # Sentence contains a time expression

            candidate_sent_list.append(sentence_list[i])

            # Now compute the wordmatch score
            score = score + 4 + WM.stemWordMatch(cleansedQuestion,sentence_list[i])
            #sent_score_list.append((score,i))

        # 2. Check if the Question contains "the last" and sentence contains any of "first,last,since,ago", then score+= slam_dunk

        for word in cleansedQuestion:
            if word.lower() in ['the','last']:
                for sent in  sentence_list[i]:
                    if sent in ['first','last','since','ago']:
                        score = score +20


            # 3. If the question contains {start,begin} and sentence contains {start,begin,since,year}
            if word.lower() in ['start','begin']:
                for sent in  sentence_list[i]:
                    if sent in ['start','begin','since','year']:
                        score = score +20

        sent_score_list[i]=score

    #print 'Candidate sentences list is :',candidate_sent_list
    #print 'Sent score list is :', sent_score_list



    # For when and where questions the answer to the question could also be from the timeline of the story

    dateline_score=0
    for i in range(0,len(cleansedQuestion)):
        # 1. If question contains "happen", it is a good clue that timeline could be answer
        if cleansedQuestion[i].lower()=='happen':
            dateline_score= dateline_score+4

        # 2. If question contains "take place", it is a good clue that timeline could be answer
        if i != len(cleansedQuestion)-1 and cleansedQuestion[i].lower()=='take' and cleansedQuestion[i+1].lower()=='place':
            dateline_score=dateline_score+4

        # 3. If question contains "this", it is slam_dunk that timeline could be answer
        if cleansedQuestion[i].lower()=='this':
            dateline_score= dateline_score+12

        # 4. If question contains "story", it is slam_dunk that timeline could be answer

        if cleansedQuestion[i].lower()=='story':
            dateline_score= dateline_score+12

    print 'Date line score for the question is :',dateline_score
    # Selecting the sentence that has the maximum score. If the dateline score is greater than max of sent_score choose
    # dateline_score else choose the maximum score from sent_score_list

    max_score_index=max(sent_score_list, key=lambda i: sent_score_list[i])

    score_values=sent_score_list.values()
    max_score_value =max(score_values)


    #print 'Max value is :', max_score_value
    # Checking which of the scores is greater. IF score from sent_Score_list is greater than dateline score, then we find
    # the corresponding sentences and choose the best among them. Else we return the dateline as the result.
    if max_score_value > dateline_score:


        # Now we have to choose the best sentence among the sentences in candidate list

        # First step is to parse the stop-words free question and look for words in the question which might help us find
        #the answer

        #print 'Stopwords free question :', stop_words_free_question

        '''for i in stop_words_free_question:
            if i in when_year:
                final_sent_list.append('''


        # Giving preference to sentences which contain a year value #
        for i in sent_score_list.keys():
            '''temp=sentence_list[i].split()
            for j in range(0, len(temp)):
                if j in when_year:
                    print 'Year is true'
                    #final_sent_list.append(sentence_list[i])
                    final_sent_list.append(j)'''

             # If none of the sentences contain a year, then choose the one with maximum value
            if sent_score_list[i]==max_score_value:
                final_sent_list.append(sentence_list[i])

        #print 'Final sentence list is:',final_sent_list


        # Now from the sentences extracting out the years or the date /time values alone and representing them
        final_temp_list=[]
        if len(final_sent_list) == 1:
            temp=nltk.word_tokenize(final_sent_list[0])
            for j in range(0, len(temp)):
                if temp[j] in when_year:
                    #print 'year true'
                    final_temp_list.append(temp[j])

            if final_temp_list != []:
                result=' '.join(final_temp_list)
                print 'Result is :', result
                return result
            else:
                print 'Result is :', final_sent_list[0]
                return final_sent_list[0]
        else:
            result=' '.join(final_sent_list)
            print 'Result is :', result
            return result

    else:
        result=dateline
        print 'Result sentence is dateline:', result
        return result



