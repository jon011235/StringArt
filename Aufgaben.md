# Implementierungsschritte

1) Vertraut machen mit dem Framework
 - Implementieren von ```printOperations```
 - Zeichne ein Quadrat in das Bild ein
 - finde die dunkelste Linie von Nagel 0 aus

2) Greedy
i = Nagel 0. 
Ziehe die dunkelste Linie die von Nagel i aus möglich ist. 
Der Nagel an dem die Linie endet ist der neue Nagel i

3) Wie könnte man den Algorithmus verbessern?
Mögliche Ansätze:
- anderes Anti-aliasing
- Vorberechnen aller möglichen Linien (falls Nagel 0 sehr ungeeignet ist)
- Kein Greedy Algorithmus (priority Queue, Fast Fourier Transformations)