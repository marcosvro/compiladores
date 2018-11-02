import numpy as np
import csv


class dict(dict):
	def define_padrao(self, valor):
		self.valor_padrao = valor
	def __missing__(self, key):
		return self.valor_padrao

class Lexico:

	def __init__ (self, arquivo_fonte):
		self.estado_inicial = '0'
		self.linha = 1
		self.coluna = 1
		self.ponteiro = 0

		self.tabela_simbolos = dict ({
			'inicio':['inicio',''],
			'varinicio':['varinicio',''],
			'varfim':['varfim',''],
			'escreva':['escreva',''],
			'leia':['leia',''],
			'se':['se',''],
			'entao':['entao',''],
			'fimse':['fimse',''],
			'fim':['fim',''],
			'int':['int',''],
			'lit':['lit',''],
			'real':['real','']
			})
		self.tabela_simbolos.define_padrao([])
		#print(self.tabela_simbolos['inicio'])

		self.lista_reconhece = dict({
			'1':'num',
			'3':'num',
			'6':'num',
			'8':'literal',
			'9':'id',
			'11':'comentário',
			'12':'EOF',
			'13':'opr',
			'14':'opr',
			'15':'opr',
			'16':'rcb',
			'17':'opm',
			'18':'ab_p',
			'19':'fc_p',
			'20':'pt_v'
			})
		self.lista_reconhece.define_padrao('ERRO')

		self.lista_erro = {
			'0':'Token inválido!',
			'2':'Token inválido: Informe um dígito após o "."',
			'4':'Token inválido: Informe um dígito com ou sem sinal após o E ou e, ex, ..36e-41',
			'5':'Token inválido: Informe um dígito após o sinal, ex, ..36e-41',
			'7':'Token inválido: Esperava " (aspas duplas)',
			'10':'Token inválido: Esperava "}"'
			}

		try:
			self.arquivo_fonte = open(arquivo_fonte)
			#print(self.arquivo_fonte)
		except Exception as e:
			print ("Erro ao abrir arquivo fonte '%s'!!"%str(arquivo_fonte))
			exit()
		try:
			with open ('tabela_de_transicoes_lexico.csv', newline='') as csvfile:
				self.tabela_lexico = list(csv.reader(csvfile, delimiter=','))
				self.tabela_lexico = np.array(self.tabela_lexico)
				
				classes_itens = self.tabela_lexico[0, 1:]
				self.classifica_item = dict()
				for idx,tipo in enumerate(classes_itens):
					if tipo == 'L':
						alfabeto = 'abcdefghijklmnopqrstuvwxyz'
						alfabeto2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
						aux = self.classifica_item
						self.classifica_item = dict.fromkeys(alfabeto, idx)
						self.classifica_item.update(dict.fromkeys(alfabeto2, idx))
						self.classifica_item.update(aux)
					elif tipo == 'D':
						numeros = '0123456789'
						aux = self.classifica_item
						self.classifica_item = dict.fromkeys(numeros, idx)
						self.classifica_item.update(aux)
					elif tipo == 'EOF':
						self.classifica_item.update({'':idx})
					elif tipo == 'espaço':
						self.classifica_item.update({' ':idx})
					elif tipo == '\\t':
						self.classifica_item.update({'\t':idx})
					elif (tipo == '\\n'):
						self.classifica_item.update({'\n':idx})
					elif (tipo == '\\.'):
						self.classifica_item.update({'.':idx})
					elif (tipo == 'any'):
						self.classifica_item.define_padrao(idx)
					else:
						self.classifica_item.update({tipo:idx})

				self.tabela_lexico = self.tabela_lexico[1:, 1:]
		except Exception as e:
			print ("Erro ao abrir tabela de transições do módulo Léxico!!")
			exit()
		
	

	def pega_token (self):
		if self.arquivo_fonte is None:
			print("Arquivo já finalizado!!")
			exit()

		estado_atual = int(self.estado_inicial)
		lexema = ''
		self.arquivo_fonte.seek(self.ponteiro)

		while(True):
			#Lê simbolo do arquivo fonte
			simbolo = self.arquivo_fonte.read(1)
			

			#procura na tabela de transições do DFA Léxico um novo estado a partir do estado atual com 'simbolo'
			j = int(self.classifica_item[simbolo])
			i = estado_atual
			#print(lexema, simbolo)
			novo_estado = self.tabela_lexico[i,j]


			if(novo_estado == ''):
				#caso a transição não exista na tabela de transições


				if self.lista_reconhece[str(estado_atual)] == 'ERRO':
					#estado atual não é de aceitação
					print("Erro na linha %d coluna %d:"%(self.linha, self.coluna))
					print(self.lista_erro[str(estado_atual)])
					exit()
				else:
					#estado atual é de aceitação, retornar token
					token = self.lista_reconhece[str(estado_atual)]
					tipo = ''

					if token == 'id':
						if self.tabela_simbolos[lexema] == []:
							#id que não existe na tabela de simbolos, inserir id
							self.tabela_simbolos.update({lexema:[token,tipo]})
							return (token, lexema, tipo)
						else:
							#lexema já existe na tabela de simbolos, retornar atributos da tabela
							[token, tipo] = self.tabela_simbolos[lexema]
							return (token, lexema, tipo)
					else:
						if lexema is '': #end of file
							self.arquivo_fonte.close()
							self.arquivo_fonte = None
						return (token, lexema, tipo)

			else:
				#caso exista uma transição do estado atual com 'simbolo'
				if simbolo == '\t':
					self.coluna += 4
				elif simbolo == ' ':
					self.coluna += 1
				elif simbolo == '\n':
					self.coluna = 1
					self.linha += 1
				else:
					lexema += simbolo
					self.coluna += 1

				estado_atual = int(novo_estado)
				self.ponteiro += 1





if __name__ == '__main__':
	a  = Lexico("test.mgol")
	while True:
		tupla = a.pega_token()
		print(tupla)
		'''
		if (tupla[0] == 'EOF'):
			print (a.tabela_simbolos)
		'''