#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 infodata
'''

'''nsDeAcertos = range(11,16); lfProbs = {}
for nDeAcerto in nsDeAcertos:
  lfProbs[nDeAcerto] = ic.comb(25,nDeAcerto)
'''

lfProbs = {15:3268760, 14:21791, 13:691, 12:59, 11:11}

lmProb20 = 11372635
lmProbs = {20:lmProb20, 19:352551, 18:24235, 17:2776,16:472,0:lmProb20}

'''nsDeAcertos = range(4,7); msProbs = {}
for nDeAcerto in nsDeAcertos:
  msProbs[nDeAcerto] = ic.comb(60,nDeAcerto)
'''
msProbs = {6:50063860, 5:154518, 4:2332}

lfComoJogar = '''A Lotofácil é o jogo certo para você que gosta de apostar e, principalmente, ganhar. Com apenas R$ 1, 25, você marca 15 números entre os 25 disponíveis no volante. E fatura o prêmio se acertar 11, 12, 13, 14 ou 15 números. São muitas chances de ganhar.

Você pode deixar ainda que o sistema escolha os números para você (Surpresinha) e/ou continuar com o seu jogo por 2, 4 ou 8 concursos consecutivos (Teimosinha). Os sorteios são realizados às segundas e quintas, sempre às 20h.

O prêmio bruto corresponde a 46% da arrecadação, já computado o adicional destinado ao Ministério do Esporte. Dessa porcentagem, será deduzido o pagamento dos prêmios com valores fixos:

    *

      R$ 2,50 para as apostas com 11 prognósticos certos entre os 15 sorteados;
    *

      R$ 5,00 para as apostas com 12 prognósticos certos entre os 15 sorteados;
    *

      R$ 12,50 para as apostas com 13 prognósticos certos entre os 15 sorteados.

Somente após a apuração dos ganhadores dos prêmios com valores fixos, o valor restante do total destinado à premiação será distribuído para as demais faixas de prêmios nos seguintes porcentuais:

    *

      70% entre os acertadores de 15 números;
    *

      30% entre os acertadores de 14 números entre os 15 sorteados.

Não havendo ganhador em qualquer faixa de premiação, o valor acumula para o concurso seguinte, na faixa de prêmio com 15 acertos. Não deixe de conferir o seu bilhete de aposta.

Os prêmios prescrevem 90 dias após a data do sorteio. Após esse prazo, os valores são repassados ao tesouro nacional para aplicação no FIES - Fundo de Financiamento ao Estudante do Ensino Superior.'''


lmComoJogar = '''Na Lotomania, você escolhe 50 números e ganha se acertar 16, 17, 18, 19, 20 ou nenhum número. Ela é simples de apostar e fácil de ganhar. Além de marcar no volante, você conta com outras formas de jogar. Você pode: apostar uma quantidade inferior a 50 números e deixar que o sistema complete o jogo para você; não marcar nada e deixar que o sistema escolha todos os números (Surpresinha) e/ou repetir o mesmo jogo por 2 ou 4 semanas (Teimosinha).

Você pode ainda efetuar uma nova aposta com o sistema selecionando os outros 50 números não registrados no jogo original (Aposta-Espelho).

O preço da aposta é único e custa apenas R$ 1,00. Os sorteios são realizados às quartas-feiras e aos sábados, às 20h. O prêmio bruto corresponde a 46% da arrecadação, já computado o adicional destinado ao Ministério do Esporte. Dessa porcentagem são distribuídos:

    *

      30% entre os acertadores dos 20 números sorteados;
    *

      20% entre os acertadores de 19 números;
    *

      20% entre os acertadores de 18 números;
    *

      10% entre os acertadores de 17 números
    *

      10% entre os acertadores de 16 números;
    *

      10% entre os apostadores que não acertaram nenhum número.

Não havendo acertador na faixa de 0 acerto, o valor acumula para o concurso seguinte, na primeira faixa de premiação correspondente a 20 acertos. Nas demais faixas ( 16, 17, 18, 19 e 20 acertos) o valor acumula para o concurso seguinte na respectiva faixa.

Os prêmios prescrevem 90 dias após a data do sorteio. Após esse prazo, os valores são repassados ao tesouro nacional para aplicação no FIES - Fundo de Financiamento ao Estudante do Ensino Superior.'''

msComoJogar = '''A Mega-Sena é o jogo que paga milhões para o acertador dos 6 números sorteados. Mas quem acerta 4 ou 5 números também ganha. Para realizar o sonho de ser o próximo milionário, você deve marcar de 6 e 15 números, entre os 60 disponíveis no volante. Você pode deixar que o sistema escolha os números para você (Surpresinha) e/ou concorrer com o mesmo jogo por 2, 4 ou 8 concursos consecutivos (Teimosinha).

Os sorteios são realizados duas vezes por semana, às quartas e aos sábados. A aposta mínima, de 6 números, custa R$ 2,00. Quanto mais números marcar, maior o preço da aposta e maiores as chances de faturar o prêmio mais cobiçado do país.

O prêmio bruto corresponde a 46% da arrecadação, já computado o adicional destinado ao Ministério do Esporte. Dessa porcentagem:

    * 35% são distribuídos entre os acertadores dos 6 números sorteados (Sena);
    * 19% entre os acertadores de 5 números (Quina);
    * 19% entre os acertadores de 4 números (Quadra);
    * 22% ficam acumulados e distribuídos aos acertadores dos 6 números nos concursos de final 0 ou 5.
    * 5% ficam acumulado para a primeira faixa - sena - do último concurso do ano de final zero ou 5 cinco. 

Não havendo acertador em qualquer faixa, o valor acumula para o concurso seguinte, na respectiva faixa de premiação. Não deixe de conferir o seu bilhete de aposta.

Os prêmios prescrevem 90 dias após a data do sorteio. Após esse prazo, os valores são repassados ao tesouro nacional para aplicação no FIES - Fundo de Financiamento ao Estudante do Ensino Superior.'''


lotsProbs = {'LF':lfProbs, 'LM':lmProbs,'MS':msProbs}
lotsComoJogar = {'LF':lfComoJogar, 'LM':lmComoJogar,'MS':msComoJogar}


def legacy1():
  num=1
  den=1
  for i in range(100,80,-1):
    num *= i
    #print 'num', num
  for i in range(50,30,-1):
    den *= i
    #print 'den', den

  prob20 = num/den
  shouldbe20 = 11372635
  print 'prob take 20 num/den', prob20
  assert(prob20 == shouldbe20)

  prob19 = prob20 * 20.0 / 81
  shouldbe19 = 352551
  print 'prob take 19 num/den', prob19
  #assert_equal(prob19, shouldbe19)
  #assert (prob19 == shouldbe19)

  n100a20=ic.iCmb(100, 20)
  n100a19=ic.iCmb(100, 19)
  r=(n100a20+0.0)/n100a19
  print r
  print 81.0/20
  #assert(float(r) == float(81.0/20))

  n50a20=ic.iCmb(50, 20)
  n50a19=ic.iCmb(50, 19)
  print 'n50a20', n50a20
  print 'n50a19', n50a19

  r = (n100a20 + 0.0) / (50*n50a19 + 0.0)
  print r

  n50a2=ic.iCmb(50, 2)
  n50a18=ic.iCmb(50, 18)
  print 'n50a2', n50a2
  print 'n50a18', n50a18

  r = (n100a20 + 0.0) / (n50a2*n50a18 + 0.0)
  print r


if __name__ == '__main__':
  pass
