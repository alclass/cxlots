#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import sys
import localpythonpath
localpythonpath.setlocalpythonpath()

from models.Concurso import ConcursoBase


distancesDictStr="{1: 41, 2: 40, 3: 61, 4: 60, 5: 59, 6: 58, 7: 57, 8: 56, 9: 55, 10: 54, 11: 53, 12: 52, 13: 51, 14: 50, 15: 49, 16: 48, 17: 47, 18: 46, 19: 45, 20: 44, 21: 43, 22: 42, 23: 41, 24: 40, 25: 39, 26: 38, 27: 37, 28: 36, 29: 35, 30: 34, 31: 33, 32: 32, 33: 31, 34: 30, 35: 29, 36: 48, 37: 47, 38: 46, 39: 45, 40: 44, 41: 43, 42: 50, 43: 49, 44: 48, 45: 47, 46: 46, 47: 45, 48: 44, 49: 43, 50: 42, 51: 41, 52: 40, 53: 39, 54: 38, 55: 37, 56: 36, 57: 35, 58: 39, 59: 38, 60: 37, 61: 36, 62: 35, 63: 34, 64: 33, 65: 32, 66: 37, 67: 36, 68: 35, 69: 34, 70: 33, 71: 32, 72: 46, 73: 45, 74: 44, 75: 43, 76: 42, 77: 41, 78: 40, 79: 39, 80: 43, 81: 42, 82: 41, 83: 40, 84: 39, 85: 38, 86: 39, 87: 38, 88: 37, 89: 36, 90: 35, 91: 34, 92: 35, 93: 36, 94: 35, 95: 48, 96: 47, 97: 46, 98: 45, 99: 44, 100: 43, 101: 42, 102: 41, 103: 40, 104: 39, 105: 38, 106: 37, 107: 36, 108: 35, 109: 34, 110: 40, 111: 39, 112: 38, 113: 37, 114: 36, 115: 36, 116: 35, 117: 34, 118: 37, 119: 36, 120: 35, 121: 34, 122: 33, 123: 32, 124: 31, 125: 30, 126: 29, 127: 28, 128: 27, 129: 26, 130: 25, 131: 24, 132: 23, 133: 27, 134: 33, 135: 32, 136: 31, 137: 31, 138: 30, 139: 29, 140: 33, 141: 32, 142: 31, 143: 30, 144: 55, 145: 54, 146: 53, 147: 52, 148: 51, 149: 50, 150: 49, 151: 48, 152: 47, 153: 46, 154: 50, 155: 49, 156: 48, 157: 47, 158: 46, 159: 45, 160: 44, 161: 43, 162: 42, 163: 41, 164: 40, 165: 39, 166: 41, 167: 40, 168: 39, 169: 38, 170: 37, 171: 36, 172: 35, 173: 34, 174: 33, 175: 32, 176: 34, 177: 33, 178: 32, 179: 31, 180: 30, 181: 29, 182: 28, 183: 27, 184: 40, 185: 39, 186: 38, 187: 37, 188: 36, 189: 35, 190: 34, 191: 33, 192: 32, 193: 31, 194: 32, 195: 31, 196: 30, 197: 29, 198: 28, 199: 32, 200: 31, 201: 30, 202: 29, 203: 28, 204: 27, 205: 26, 206: 25, 207: 41, 208: 40, 209: 39, 210: 38, 211: 37, 212: 36, 213: 35, 214: 34, 215: 33, 216: 32, 217: 31, 218: 30, 219: 35, 220: 34, 221: 51, 222: 50, 223: 49, 224: 48, 225: 47, 226: 46, 227: 45, 228: 44, 229: 43, 230: 45, 231: 44, 232: 43, 233: 42, 234: 41, 235: 40, 236: 39, 237: 38, 238: 37, 239: 36, 240: 35, 241: 34, 242: 33, 243: 32, 244: 31, 245: 30, 246: 29, 247: 30, 248: 40, 249: 39, 250: 38, 251: 37, 252: 36, 253: 44, 254: 43, 255: 42, 256: 41, 257: 40, 258: 39, 259: 38, 260: 37, 261: 36, 262: 35, 263: 34, 264: 52, 265: 51, 266: 50, 267: 49, 268: 48, 269: 47, 270: 46, 271: 45, 272: 44, 273: 43, 274: 42, 275: 41, 276: 40, 277: 39, 278: 38, 279: 51, 280: 50, 281: 49, 282: 48, 283: 47, 284: 46, 285: 45, 286: 44, 287: 43, 288: 42, 289: 41, 290: 40, 291: 39, 292: 38, 293: 37, 294: 36, 295: 63, 296: 62, 297: 61, 298: 60, 299: 59, 300: 58, 301: 57, 302: 56, 303: 55, 304: 54, 305: 53, 306: 52, 307: 51, 308: 50, 309: 49, 310: 48, 311: 47, 312: 46, 313: 45, 314: 44, 315: 43, 316: 42, 317: 41, 318: 40, 319: 39, 320: 39, 321: 38, 322: 37, 323: 36, 324: 35, 325: 34, 326: 52, 327: 51, 328: 50, 329: 49, 330: 48, 331: 47, 332: 46, 333: 45, 334: 44, 335: 43, 336: 42, 337: 41, 338: 40, 339: 39, 340: 38, 341: 37, 342: 36, 343: 35, 344: 34, 345: 42, 346: 50, 347: 49, 348: 48, 349: 47, 350: 61, 351: 60, 352: 59, 353: 58, 354: 57, 355: 56, 356: 55, 357: 54, 358: 53, 359: 52, 360: 51, 361: 50, 362: 49, 363: 48, 364: 47, 365: 46, 366: 45, 367: 44, 368: 43, 369: 42, 370: 43, 371: 42, 372: 41, 373: 40, 374: 39, 375: 38, 376: 37, 377: 36, 378: 83, 379: 82, 380: 81, 381: 80, 382: 79, 383: 78, 384: 77, 385: 76, 386: 75, 387: 74, 388: 73, 389: 72, 390: 71, 391: 70, 392: 69, 393: 68, 394: 67, 395: 66, 396: 65, 397: 64, 398: 63, 399: 62, 400: 61, 401: 60, 402: 59, 403: 58, 404: 57, 405: 56, 406: 55, 407: 54, 408: 53, 409: 52, 410: 51, 411: 50, 412: 49, 413: 48, 414: 47, 415: 46, 416: 45, 417: 44, 418: 43, 419: 42, 420: 54, 421: 53, 422: 62, 423: 61, 424: 60, 425: 59, 426: 58, 427: 57, 428: 56, 429: 55, 430: 54, 431: 53, 432: 52, 433: 51, 434: 50, 435: 49, 436: 48, 437: 47, 438: 46, 439: 45, 440: 44, 441: 43, 442: 55, 443: 54, 444: 53, 445: 52, 446: 51, 447: 50, 448: 49, 449: 48, 450: 47, 451: 46, 452: 45, 453: 44, 454: 43, 455: 42, 456: 41, 457: 40, 458: 39, 459: 38, 460: 37, 461: 36, 462: 35, 463: 39, 464: 38, 465: 37, 466: 36, 467: 42, 468: 41, 469: 40, 470: 39, 471: 38, 472: 37, 473: 36, 474: 41, 475: 40, 476: 39, 477: 38, 478: 37, 479: 36, 480: 46, 481: 45, 482: 44, 483: 43, 484: 42, 485: 41, 486: 40, 487: 39, 488: 38, 489: 37, 490: 36, 491: 44, 492: 47, 493: 46, 494: 45, 495: 44, 496: 59, 497: 58, 498: 57, 499: 62, 500: 61, 501: 60, 502: 59, 503: 58, 504: 57, 505: 56, 506: 56, 507: 55, 508: 54, 509: 53, 510: 52, 511: 51, 512: 50, 513: 49, 514: 48, 515: 47, 516: 46, 517: 45, 518: 44, 519: 43, 520: 42, 521: 41, 522: 40, 523: 39, 524: 38, 525: 43, 526: 52, 527: 51, 528: 89, 529: 88, 530: 87, 531: 86, 532: 85, 533: 84, 534: 83, 535: 82, 536: 81, 537: 80, 538: 79, 539: 78, 540: 77, 541: 76, 542: 75, 543: 74, 544: 73, 545: 72, 546: 71, 547: 70, 548: 69, 549: 68, 550: 67, 551: 66, 552: 65, 553: 64, 554: 63, 555: 62, 556: 61, 557: 60, 558: 59, 559: 58, 560: 57, 561: 56, 562: 55, 563: 54, 564: 53, 565: 52, 566: 51, 567: 50, 568: 49, 569: 48, 570: 47, 571: 46, 572: 45, 573: 44, 574: 43, 575: 42, 576: 41, 577: 40, 578: 39, 579: 38, 580: 37, 581: 36, 582: 60, 583: 59, 584: 58, 585: 57, 586: 56, 587: 55, 588: 54, 589: 53, 590: 52, 591: 51, 592: 50, 593: 49, 594: 48, 595: 47, 596: 46, 597: 45, 598: 44, 599: 43, 600: 42, 601: 41, 602: 40, 603: 39, 604: 38, 605: 37, 606: 56, 607: 55, 608: 54, 609: 53, 610: 52, 611: 51, 612: 68, 613: 67, 614: 66, 615: 65, 616: 64, 617: 63, 618: 62, 619: 61, 620: 60, 621: 59, 622: 58, 623: 57, 624: 56, 625: 55, 626: 54, 627: 53, 628: 52, 629: 51, 630: 50, 631: 49, 632: 48, 633: 47, 634: 46, 635: 45, 636: 44, 637: 43, 638: 42, 639: 41, 640: 40, 641: 39, 642: 38, 643: 42, 644: 41, 645: 40, 646: 39, 647: 47, 648: 46, 649: 45, 650: 44, 651: 43, 652: 42, 653: 41, 654: 40, 655: 39, 656: 38, 657: 37, 658: 36, 659: 35, 660: 34, 661: 33, 662: 32, 663: 31, 664: 30, 665: 29, 666: 28, 667: 36, 668: 35, 669: 34, 670: 33, 671: 32, 672: 37, 673: 36, 674: 70, 675: 69, 676: 68, 677: 67, 678: 66, 679: 65, 680: 64, 681: 63, 682: 62, 683: 61, 684: 60, 685: 59, 686: 58, 687: 57, 688: 56, 689: 55, 690: 54, 691: 53, 692: 52, 693: 51, 694: 50, 695: 49, 696: 48, 697: 47, 698: 46, 699: 45, 700: 44, 701: 43, 702: 42, 703: 41, 704: 40, 705: 39, 706: 38, 707: 37, 708: 36, 709: 35, 710: 44, 711: 43, 712: 42, 713: 41, 714: 40, 715: 39, 716: 38, 717: 37, 718: 36, 719: 35, 720: 34, 721: 33, 722: 32, 723: 31, 724: 30, 725: 40, 726: 39, 727: 38, 728: 37, 729: 40, 730: 39, 731: 38, 732: 37, 733: 36, 734: 35, 735: 34, 736: 37, 737: 36, 738: 45, 739: 44, 740: 50, 741: 49, 742: 48, 743: 47, 744: 46, 745: 45, 746: 44, 747: 43, 748: 42, 749: 41, 750: 40, 751: 39, 752: 38, 753: 37, 754: 36, 755: 35, 756: 52, 757: 51, 758: 50, 759: 49, 760: 48, 761: 47, 762: 46, 763: 45, 764: 53, 765: 52, 766: 51, 767: 50, 768: 49, 769: 48, 770: 47, 771: 46, 772: 45, 773: 44, 774: 43, 775: 42, 776: 41, 777: 40, 778: 39, 779: 38, 780: 37, 781: 36, 782: 35, 783: 34, 784: 33, 785: 42, 786: 41, 787: 40, 788: 39, 789: 38, 790: 37, 791: 36, 792: 35, 793: 34, 794: 40, 795: 39, 796: 38, 797: 37, 798: 62, 799: 61, 800: 73, 801: 72, 802: 71, 803: 70, 804: 69, 805: 68, 806: 67, 807: 66, 808: 65, 809: 64, 810: 63, 811: 62, 812: 61, 813: 60, 814: 59, 815: 58, 816: 57, 817: 56, 818: 55, 819: 54, 820: 53, 821: 52, 822: 51, 823: 50, 824: 49, 825: 48, 826: 47, 827: 46, 828: 45, 829: 44, 830: 43, 831: 42, 832: 41, 833: 40, 834: 44, 835: 43, 836: 42, 837: 41, 838: 40, 839: 39, 840: 38, 841: 37, 842: 36, 843: 35, 844: 34, 845: 33, 846: 32, 847: 31, 848: 30, 849: 29, 850: 28, 851: 40, 852: 40, 853: 59, 854: 58, 855: 57, 856: 56, 857: 55, 858: 54, 859: 53, 860: 52, 861: 51, 862: 50, 863: 49, 864: 48, 865: 47, 866: 46, 867: 45, 868: 44, 869: 43, 870: 42, 871: 41, 872: 40, 873: 39, 874: 38, 875: 37, 876: 36, 877: 35, 878: 34, 879: 33, 880: 49, 881: 48, 882: 47, 883: 46, 884: 45, 885: 44, 886: 43, 887: 42, 888: 41, 889: 40, 890: 39, 891: 38, 892: 37, 893: 36, 894: 35, 895: 34, 896: 33, 897: 45, 898: 44, 899: 43, 900: 42, 901: 41, 902: 68, 903: 67, 904: 66, 905: 65, 906: 64, 907: 63, 908: 62, 909: 61, 910: 60, 911: 59, 912: 58, 913: 57, 914: 56, 915: 55, 916: 54, 917: 53, 918: 52, 919: 56, 920: 55, 921: 54, 922: 54, 923: 53, 924: 52, 925: 51, 926: 50, 927: 49, 928: 48, 929: 47, 930: 46, 931: 45, 932: 44, 933: 43, 934: 42, 935: 41, 936: 40, 937: 44, 938: 43, 939: 42, 940: 41, 941: 40, 942: 43, 943: 42, 944: 41, 945: 40, 946: 39, 947: 38, 948: 37, 949: 36, 950: 58, 951: 57, 952: 56, 953: 55, 954: 54, 955: 53, 956: 52, 957: 51, 958: 50, 959: 49, 960: 48, 961: 47, 962: 46, 963: 45, 964: 44, 965: 43, 966: 42, 967: 41, 968: 40, 969: 39, 970: 76, 971: 75, 972: 74, 973: 73, 974: 72, 975: 71, 976: 70, 977: 69, 978: 68, 979: 67, 980: 66, 981: 65, 982: 64, 983: 63, 984: 62, 985: 61, 986: 60, 987: 59, 988: 58, 989: 57, 990: 56, 991: 55, 992: 54, 993: 53, 994: 52, 995: 51, 996: 50, 997: 49, 998: 48, 999: 47, 1000: 46, 1001: 48, 1002: 47, 1003: 46, 1004: 45, 1005: 44, 1006: 43, 1007: 42, 1008: 41, 1009: 40, 1010: 39, 1011: 38, 1012: 37, 1013: 36, 1014: 35, 1015: 34, 1016: 33, 1017: 32, 1018: 31, 1019: 43, 1020: 42, 1021: 44, 1022: 43, 1023: 42, 1024: 41, 1025: 40, 1026: 39, 1027: 38, 1028: 37, 1029: 36, 1030: 35, 1031: 34, 1032: 33, 1033: 32, 1034: 31, 1035: 30, 1036: 29, 1037: 28, 1038: 27, 1039: 26, 1040: 25, 1041: 24, 1042: 32, 1043: 45, 1044: 44, 1045: 60, 1046: 59, 1047: 58, 1048: 57, 1049: 56, 1050: 55, 1051: 60, 1052: 59, 1053: 58, 1054: 57, 1055: 56, 1056: 55, 1057: 54, 1058: 53, 1059: 52, 1060: 51, 1061: 50, 1062: 49, 1063: 48, 1064: 51, 1065: 50, 1066: 49, 1067: 48, 1068: 47, 1069: 46, 1070: 45, 1071: 44, 1072: 43, 1073: 42, 1074: 41, 1075: 40, 1076: 39, 1077: 38, 1078: 37, 1079: 36, 1080: 35, 1081: 34, 1082: 33, 1083: 32, 1084: 31, 1085: 43, 1086: 42, 1087: 41, 1088: 40, 1089: 39, 1090: 38, 1091: 37, 1092: 36, 1093: 35, 1094: 34, 1095: 33, 1096: 32, 1097: 31, 1098: 51, 1099: 50, 1100: 78, 1101: 77, 1102: 76, 1103: 75, 1104: 74, 1105: 73, 1106: 72, 1107: 71, 1108: 70, 1109: 69, 1110: 68, 1111: 67, 1112: 66, 1113: 65, 1114: 64, 1115: 63, 1116: 62, 1117: 61, 1118: 60, 1119: 59, 1120: 58, 1121: 57, 1122: 56, 1123: 55, 1124: 55, 1125: 54, 1126: 53, 1127: 53, 1128: 52, 1129: 51, 1130: 50, 1131: 49, 1132: 48, 1133: 47, 1134: 46, 1135: 45, 1136: 44, 1137: 43, 1138: 42, 1139: 41, 1140: 40, 1141: 39, 1142: 38, 1143: 37, 1144: 36, 1145: 35, 1146: 34, 1147: 33, 1148: 32, 1149: 45, 1150: 44, 1151: 43, 1152: 42, 1153: 41, 1154: 40, 1155: 39, 1156: 41, 1157: 40, 1158: 39, 1159: 38, 1160: 37, 1161: 36, 1162: 35, 1163: 34, 1164: 33, 1165: 32, 1166: 31, 1167: 30, 1168: 29, 1169: 28, 1170: 54, 1171: 53, 1172: 52, 1173: 51, 1174: 50, 1175: 49, 1176: 48, 1177: 47, 1178: 46, 1179: 45, 1180: 44, 1181: 43, 1182: 51, 1183: 50, 1184: 49, 1185: 48, 1186: 47, 1187: 46, 1188: 45, 1189: 65, 1190: 64, 1191: 63, 1192: 62, 1193: 61, 1194: 60, 1195: 59, 1196: 58, 1197: 57, 1198: 56, 1199: 55, 1200: 54, 1201: 53, 1202: 52, 1203: 51, 1204: 50, 1205: 49, 1206: 48, 1207: 53, 1208: 52, 1209: 51, 1210: 50, 1211: 49, 1212: 48, 1213: 47, 1214: 46, 1215: 45, 1216: 44, 1217: 43, 1218: 42, 1219: 41, 1220: 40, 1221: 39, 1222: 38, 1223: 37, 1224: 36, 1225: 36, 1226: 35, 1227: 38, 1228: 37, 1229: 36, 1230: 35, 1231: 34, 1232: 33, 1233: 32, 1234: 31, 1235: 30, 1236: 33, 1237: 32, 1238: 37, 1239: 36, 1240: 35, 1241: 37, 1242: 36, 1243: 35, 1244: 45, 1245: 62, 1246: 61, 1247: 60, 1248: 59, 1249: 58, 1250: 57, 1251: 56, 1252: 55, 1253: 54, 1254: 53, 1255: 52, 1256: 51, 1257: 50, 1258: 49, 1259: 48, 1260: 47, 1261: 46, 1262: 45, 1263: 44, 1264: 43, 1265: 53, 1266: 52, 1267: 51, 1268: 53, 1269: 52, 1270: 51, 1271: 50, 1272: 49, 1273: 48, 1274: 47, 1275: 46, 1276: 45, 1277: 44, 1278: 43, 1279: 42, 1280: 41, 1281: 40, 1282: 39, 1283: 38, 1284: 37, 1285: 38, 1286: 37, 1287: 36, 1288: 35, 1289: 34, 1290: 33, 1291: 32, 1292: 31, 1293: 32, 1294: 48, 1295: 47, 1296: 46, 1297: 45, 1298: 44, 1299: 43, 1300: 42, 1301: 41, 1302: 40, 1303: 41, 1304: 40, 1305: 39, 1306: 38, 1307: 37, 1308: 36, 1309: 35, 1310: 34, 1311: 33, 1312: 35, 1313: 34, 1314: 33, 1315: 48, 1316: 47, 1317: 46, 1318: 45, 1319: 73, 1320: 72, 1321: 71, 1322: 70, 1323: 69, 1324: 68, 1325: 67, 1326: 66, 1327: 65, 1328: 64, 1329: 63, 1330: 62, 1331: 61, 1332: 60, 1333: 59, 1334: 58, 1335: 57, 1336: 56, 1337: 55, 1338: 54, 1339: 53, 1340: 52, 1341: 51, 1342: 50, 1343: 49, 1344: 48, 1345: 47, 1346: 46, 1347: 45, 1348: 44, 1349: 43, 1350: 42, 1351: 41, 1352: 61, 1353: 60, 1354: 59, 1355: 58, 1356: 57, 1357: 56, 1358: 55, 1359: 54, 1360: 53, 1361: 52, 1362: 51, 1363: 50, 1364: 49, 1365: 48, 1366: 47, 1367: 46, 1368: 45, 1369: 44, 1370: 43, 1371: 42, 1372: 41, 1373: 40, 1374: 39, 1375: 38, 1376: 37, 1377: 38, 1378: 37, 1379: 36, 1380: 35, 1381: 34, 1382: 33, 1383: 32}"
# do an eval (dynamic initialization) so that Eclipse will not get too slow!
distancesDict=eval(distancesDictStr)

class DistanceAllOccurrred(object):
  '''
  The idea behind this metric is to measure the number of concursos, from a past concurso onwards, all dozens appear.
  Eg. It took 41 concursos at the beginning of Megasena for all 60 dozens appear (at least one, which happens for at least one dozen)
  As of this time, max "spike-distance", as it is called, is 87. Min is 27.  Average is around 41/42.
  '''
  
  def __init__(self):
    self.distancesDict = {}
    self.frequencies_within_spike_range = {}
    self.spiked_tuple_list = None  # eg. [(1,40),(3,60),(36,47),(42,49)...]
    self.concursoBase = ConcursoBase()
    self.process()
    #self.distancesDict = distancesDict    
    self.summarize()
    
  def process(self):
    FINISH_PROCESSING = False
    for parked_nDoConc in range(1, self.concursoBase.get_total_concursos() + 1):
      # print 'Processing DistanceAllOccurrred metric:', parked_nDoConc, 
      concurso = self.concursoBase.get_concurso_by_nDoConc(parked_nDoConc) # concurso_parked
      all_dezenas_frequency_dict = DezenasVolanteFrequencyDict(self.concursoBase.N_DE_DEZENAS_NO_VOLANTE)
      all_dezenas_frequency_dict.add_1_to_values_given_key_list(concurso.get_dezenas())
      distance = 1
      while 1:
        if not all_dezenas_frequency_dict.is_there_still_a_zero_among_values():
          # print parked_nDoConc, ':: n of concs that span occurences of all dozens = ', distance
          self.distancesDict[parked_nDoConc] = distance 
          self.frequencies_within_spike_range[parked_nDoConc] = all_dezenas_frequency_dict.extract_frequencies_in_order()
          print ' >>>>>>>>> freq within spike', self.frequencies_within_spike_range[parked_nDoConc]
          break
        concurso = concurso.get_next()
        if concurso == None:
          FINISH_PROCESSING = True
          self.frequencies_within_spike_range[parked_nDoConc] = all_dezenas_frequency_dict.extract_frequencies_in_order()
          break
        all_dezenas_frequency_dict.add_1_to_values_given_key_list(concurso.get_dezenas())
        # print 'all_dezenas_dict', all_dezenas_dict 
        distance += 1
    if FINISH_PROCESSING:
      return

  def get_last_nDoConc_that_has_distance(self):
    pass
    nDoConcWithDistanceTupleList = self.distancesDict.items()
    # nDoConcWithDistanceTupleList.sort( key lambda x,y: )
    return nDoConcWithDistanceTupleList

  def compact_distanceDict_into_spikes(self):
    '''
    This metric generally happens in a decreasing manner, one by one, until a "spike"
     # eg. [(1,39),(3,59),(36,46),(42,48)...]
     The example (eg) can be read as such:
     - conc 1 needs another 38 concs to have all dozens happen at least once, ie, have every one of them occurring
     - conc 2, though it's not there, needs another 37 (ie, 38-1)
     - conc 3 "spikes" needing another 58 concs
     - from conc 4 to conc 35, distance diminishes one by one, ie, (4,58),(5,57),...,(35,27)
     - conc 36 "spikes" again
    '''
    self.spiked_tuple_list = []
    frequencies_within_spike_range_to_retain = {}
    if self.distancesDict.items() == 0:
      return
    nDoConcWithDistanceTupleList = self.distancesDict.items()
    first_spiked = nDoConcWithDistanceTupleList[0]
    self.spiked_tuple_list = [first_spiked]
    for i, nDoConcWithDistanceTuple in enumerate(nDoConcWithDistanceTupleList[1:]):
      previous_distance = nDoConcWithDistanceTupleList[i][1]
      distance = nDoConcWithDistanceTuple[1] 
      if previous_distance != distance + 1:  # CAUTION: the "i" here is tricky, because index starts looping at 1. whereas i (from enumerate()) starts at 0
        # this means: a spike happened, so register it
        self.spiked_tuple_list.append(nDoConcWithDistanceTuple)
        nDoConc = nDoConcWithDistanceTuple[0]
        frequencies_within_spike_range_to_retain[nDoConc] = self.frequencies_within_spike_range[nDoConc][:] # must be a hard copy, for right-side object will be reassigned
    # self.frequencies_within_spike_range will have only the spikes, not all history
    self.frequencies_within_spike_range = frequencies_within_spike_range_to_retain          
    self.generate_stats()
      
  def generate_stats(self):
    self.spiked_nDoConcs, self.spiked_distances = zip(*self.get_spiked_tuple_list())
    self.spiked_distances = numpy.array(self.spiked_distances)
    self.max_distance = max(self.spiked_distances)
    self.min_distance = min(self.spiked_distances)
    self.avg_distance = self.spiked_distances.mean()
    self.std_distance = self.spiked_distances.std()

  def get_spiked_tuple_list(self, reprocess=False):
    if self.spiked_tuple_list != None and not reprocess:
      return self.spiked_tuple_list
    self.compact_distanceDict_into_spikes()
    return self.spiked_tuple_list

  def summarize(self):
    print self.distancesDict
    print self.get_spiked_tuple_list()
    for nDoConc in self.frequencies_within_spike_range: print nDoConc, self.frequencies_within_spike_range[nDoConc] 
    print 'max', self.max_distance
    print 'min', self.min_distance
    print 'avg', self.avg_distance
    print 'std', self.std_distance
    print 'strides', self.spiked_distances.strides
    #print 'cumsum', self.spiked_distances.cumsum()
    print 'len spiked list', len(self.get_spiked_tuple_list())


class DezenasVolanteFrequencyDict(dict):
  '''
  This class inherits from dict, adding some "custom" functionality to it
  These "custom" functionalities are:
  
  1) at construction time: initialize a 1 to n array mapping with zeroes, ie, d[1]=0, d[2]=0, ... , d[n]=0
   
  2) add 1 to every element in a subset of [1, ..., n], eg, add_1_to([7,19,33]) means d[7]+=1, d[19]+=1 and d[33]+=1
  
  3) is_there_still_a_zero_among_values() means what it says, is there an element e such that d[e] is (still) equal to 0?  If there is, return True, otherwise, return False
  
  4) extract_frequencies_in_order() extracts an array with the frequencies in the ascending order of the mapping elements (1 to n)
     Eg. Suppose this subset {4:23, 1:25, 33:24}, extraction then would result in the tuple (25, 23, 24)
     (Of course, we sampled a subset, the whole set has n elements (1, 2, ... , n) :: the one in the example is incomplete, having only (1,4,33) 
     
  Notice that the objects from the class just work normally as a dict-typed object! 
  '''
  
  def __init__(self, n_elems):
    super(DezenasVolanteFrequencyDict, self).__init__()
    self.n_elems = n_elems
    self.zero_dict_values_key_index_start_at_1_to_n()

  def zero_dict_values_key_index_start_at_1_to_n(self):
    for i in range(1, self.n_elems + 1): self[i] = 0
  
  def add_1_to_values_given_key_list(self, keys):
    for i in keys: self[i] += 1
  
  def is_there_still_a_zero_among_values(self):
    if 0 in self.values():
      return True
    return False
  
  def extract_frequencies_in_order(self):
    tuple_list = self.items()
    tuple_list.sort( key = lambda x: x[0] )
    freqs = zip(*tuple_list)[1]
    audit_dozen_freq_pair(self, freqs)
    return freqs

  def incorporate_dict(self, p_dict):
    for k in p_dict:
      self[k] = p_dict[k]

def audit_dozen_freq_pair(p_dict, freqs):
  for i, freq in enumerate(freqs):
    dezena = i + 1
    if p_dict[dezena] != freq:
      error_msg = 'Audit routine found a problem during transposing freqs from dict :: p_dict[dezena=%d]=%d != freq=%d' %(dezena, p_dict[dezena], freq)
      raise ValueError, error_msg 

def zero_dict_values_key_index_start_at_1_to_n(p_dict, n_elems):
  for i in range(1, n_elems + 1): p_dict[i] = 0

def add_one_to_dict_values_with_given_key_list(p_dict, keys):
  for key in keys: p_dict[key] += 1

def is_there_still_a_zero_in_dict(p_dict):
  if 0 in p_dict.values():
    return True
  return False

def extract_frequencies_in_order(p_dict):
  tuple_list = p_dict.items()
  tuple_list.sort( key = lambda x: x[0] )
  freqs = zip(*tuple_list)[1]
  audit_dozen_freq_pair(p_dict, freqs)
  return freqs

def adhoc_test():
  print 'Running list_dist_xysum_metric_thry_ms_history()'
  DistanceAllOccurrred()
  #print 'dao.distances', dao.distances

def adhoc_test2():
  print 'Testing VolanteDict'
  ddict = DezenasVolanteFrequencyDict(ConcursoBase.N_DE_DEZENAS_NO_VOLANTE)
  print 'ddict', ddict
  ddict.add_1_to_values_given_key_list([1,2,5,8,29, 45])
  print 'ddict', ddict
  print 'ddict.is_there_still_a_zero_in_dict()', ddict.is_there_still_a_zero_among_values()
  print 'adding 1 to range...'
  print 'ddict', ddict
  ddict.add_1_to_values_given_key_list(range(1, 61))
  print 'ddict', ddict
  print 'ddict.is_there_still_a_zero_in_dict()', ddict.is_there_still_a_zero_among_values()
  print 'extract_frequencies_in_order()', ddict.extract_frequencies_in_order()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
