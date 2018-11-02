import csv
import numpy as np
from lexico import Lexico

class Sintatico():

	def __init__(self, arquivo_fonte):
		self.lexico = Lexico(arquivo_fonte)

		self.producoes = {
		'2':['P', ['inicio', 'V', 'A']],
		'3':['V', ['varinicio', 'LV']],
		'4':['LV', ['D', 'LV']],
		'5':['LV', ['varfim', ';']],
		'6':['D', ['id', 'TIPO', ';']],
		'7':['TIPO', ['int']],
		'8':['TIPO', ['real']],
		'9':['TIPO', ['lit']],
		'10':['A', ['ES', 'A']],
		'11':['ES', ['leia', 'id', ';']],
		'12':['ES', ['escreva', 'ARG', ';']],
		'13':['ARG', ['literal']],
		'14':['ARG', ['num']],
		'15':['ARG', ['id']],
		'16':['A', ['CMD', 'A']],
		'17':['CMD', ['id', 'rcb', 'LD', ';']],
		'18':['LD', ['OPRD', 'opm', 'OPRD']],
		'19':['LD', ['OPRD']],
		'20':['OPRD', ['id']],
		'21':['OPRD', ['num']],
		'22':['A', ['COND', 'A']],
		'23':['COND', ['CABEÇALHO', 'CORPO']],
		'24':['CABEÇALHO', ['se', '(', 'EXP_R', ')', 'entao']],
		'25':['EXP_R', ['OPRD', 'opr', 'OPRD']],
		'26':['CORPO', ['ES', 'CORPO']],
		'27':['CORPO', ['CMD', 'CORPO']],
		'28':['CORPO', ['COND', 'CORPO']],
		'29':['CORPO', ['fimse']],
		'30':['A', ['fim']]
		}

		try:
			with open ('tabela_shift_reduce.csv', newline='') as csvfile:
				self.tabela_sintatico = list(csv.reader(csvfile, delimiter=','))
				self.tabela_sintatico = np.array(self.tabela_sintatico)
				
				classes_itens = self.tabela_sintatico[0, 1:]
				self.classifica_item = dict()
				for idx,tipo in enumerate(classes_itens):
					if tipo == '$':
						self.classifica_item.update({'EOF':idx})
					elif tipo == ';':
						self.classifica_item.update({'pt_v':idx})
					elif tipo == '(':
						self.classifica_item.update({'ab_p':idx})
					elif tipo == ')':
						self.classifica_item.update({'fc_p':idx})
					else:
						self.classifica_item.update({tipo:idx})

				self.tabela_sintatico = self.tabela_sintatico[1:, 1:]
		except Exception as e:
			raise e
			print ("Erro ao abrir tabela de shift reduce do módulo Sintático!!")
			exit()


	def gera_arvore_sintatica(self):
		tupla_token = self.lexico.pega_token()
		a = self.classifica_item[tupla_token[0]]
		pilha = [0]
		derivacoes = []

		while 1:
			s = pilha.pop()
			pilha.append(s)
			#print(s, a)
			acao = self.tabela_sintatico[s, int(a)]
			if acao == '':
				#erro
				print("Deu ruim!!")
				exit()
			elif acao[0] == 's':
				pilha.append(int(acao[1:]))
				tupla_token = self.lexico.pega_token()
				a = self.classifica_item[tupla_token[0]]
			elif acao[0] == 'r':
				p = self.producoes[acao[1:]]
				for i in range(len(p[1])):
					pilha.pop()

				t = pilha.pop()
				pilha.append(t)
				#print ("estado adicionado pela redução ", t, self.classifica_item[p[0]])
				pilha.append(int(self.tabela_sintatico[t, self.classifica_item[p[0]]]))
				derivacoes.append([acao[1:], p])
				print ("%s %s -> "%(acao[1:], p[0]) + ' '.join(p[1]))
			elif acao == 'acc':
				return derivacoes



if __name__ == '__main__':
	a = Sintatico('test.mgol')
	b = a.gera_arvore_sintatica()