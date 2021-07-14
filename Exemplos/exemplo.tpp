{inteiro: m
flutuante: n}

{inteiro somaIntervaloNM (inteiro: m, inteiro: n)
    inteiro: soma, x
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
fim}

{inteiro principal ()
    inteiro: m, n
    leia(m)
    leia(n)
    escreva(somaIntervaloNM(m, n))
		retorna(0)
fim}

inteiro somaIntervaloNM (inteiro: m, inteiro: n)
    inteiro: soma
    soma:= 8
    retorna(soma)
fim

inteiro principal ()
    inteiro: m, n, x
    m:= 2
    n:= 5
    {n:= m + 3}
    x:= somaIntervaloNM(m, n)
    retorna(x)
fim

