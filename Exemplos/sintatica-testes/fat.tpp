

inteiro fatorial(inteiro: n)
    inteiro: fat
		n:= 6
    se n > 0 então {não calcula se n > 0}
        fat := 1
        repita
            fat := fat * n
            n := n - 1
        até n = 0
        retorna(fat) {retorna o valor do fatorial de n}
    senão
        retorna(1)
    fim
fim

inteiro principal()
    inteiro: n
    n:= 6
    escreva(fatorial(n))
    retorna(0)
fim
