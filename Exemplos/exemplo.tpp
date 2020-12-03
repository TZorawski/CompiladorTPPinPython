inteiro: m
flutuante: n

{inteiro somaIntervaloNM (inteiro: m, inteiro: n)
    inteiro: soma
    se m < n então
        soma := m
        repita
            m := m + 1
            soma := soma + m
        até m = n
    senão
        retorna(0)
    fim
    retorna(soma)
fim

inteiro principal ()
    {inteiro: m, n}
    leia(m)
    leia(n)
    escreva(somaIntervaloNM(m, n))
		retorna(0)
fim}

inteiro principal ()
    {inteiro: m, n}
    m:= 2
    n:= 6 + m
    retorna(0)
fim

