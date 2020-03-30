#Skripty k FYKOSímu příjmu řešení (+rozobálkování)

>> autoprijem.py -D --login jmeno_na_serveru
na stahování samotných řešení ze serveru, vyžaduje login
dřív uměl argumentem -J i spojovat řešení do jednoho souboru, ale to moc nefunguje, viz níž.

>> switch.py 
Stáhnutá řešní jsou pojmenovaná ve formátu "jméno_příjmení..."
přehodí je, aby řešení byla správně abecedně seřazená "přijmení_jméno". U řešitelů, kteří mají 3+ jmen se zeptá na input od uživatele, které je příjmení.
perlička: "ch" se v systému v angličtině řadí pod "c", takže tento skript nahradí "ch" na začátku jména za "hz"

>> pdfjoin_exceptions_split.py
Skript na elekronický příjem v době koronaviru. Řešení, která jsou ve správné podsložce "/download/rocnik{rocnik}/serie{serie}/uloha-{problem}/" (na ročník a sérii se hned zeptá, úlohy sám iteruje) spojí do jednoho souboru, resp. osmi — jeden pro každou úlohu (ve složce serie, jméno ve stylu "joined_uloha-{problem}.pdf").
Vždycky se stane, že někdo odevzdá řešení ve formátu, které tento skript nezvládne mergnout. Taková řešení skript posbírá a hodí do složky (kterou vytvoří) "/download/rocnik{rocnik}/serie{serie}/exceptions/uloha-{problem}". Doporučuji do těchto složek pak přidat věci, co prijdou mailem a poštou a všechno to pak mergnout do jednoho souboru (random online convertorem).
Zároveň si skript vytvoří "/download/rocnik{rocnik}/serie{serie}/stranyprorozdeleni_uloha-{problem}.txt", kam uloží počet stran a pořadí řešitelů v jednotlivých joined souborech, což se celkem hodí na rozdělování.

>> pdf_exceptions_together.py
Původní skript na normální příjem s fyzickým obálkováním - dělá to samé jako ten předchozí, jen:
1) exceptions nedělí po úlohách, ale nacpe je do jedné složky, aby se to dalo všechno vytisknout najednou
2) nepamatuje si počet stran jednotlivých řešitelů, takže se to pak nedá snadno rozdělit

>> pdfsplit.py
natáhne opravené joined soubory z "/corrected/rocnik{rocnik}/serie{serie}/joined_uloha-{problem}.pdf" (na ročník a sérii se zeptá) a díky souboru, co vytvořil pdfjoin_exceptions_split.py je zase rozpojí na jednotlivé řešitele a rozřadí do složek pod "/corrected/..."
