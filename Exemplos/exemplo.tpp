inteiro: m, n

inteiro somaIntervaloNM (inteiro: m, n)
    inteiro: soma
    se m < n então {apenas calcula se m > n}
        soma := m
        repita
            m := m + 1
            soma := soma + m
        até m = n
    senão {se m < n retorna zero}
        retorna(0)
    fim
    retorna(soma)
fim

inteiro principal ()
    leia(m)
    leia(n)
    escreva(somaIntervaloNM(m, n))
fim

{
    {
        a
        b
        c
    }
}
