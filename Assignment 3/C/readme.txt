Included are three files:
    1. Automata.py
        This is a class file for an automata.

    2. input.txt
        This is the input file. Format of the input is as follows:
            line1: alphabet separated by single spaces. eg- a b c d 1 2 3
            line2: regular expression that requires testing. the regex uses three operations- union (|), closure (*) and concatenation (.).
                   please enter correct regex with all operators in the right places, else the program will not work as expected.
            line3: string that requires testing.
        note: please don't add any other text to the file.

        eg- 0 1
            (0|(1.(0.1*.(0.0)*.0)*.1)*)*
            1111
            ---------------
        eg- a b c
            (a|b)*.a.b.a
            abbbaba

    3. regex.py
        After making complete changes to input.txt, run "python regex.py" on command line.
        Output is "Yes" if the string belongs to the regex or "No" otherwise.
