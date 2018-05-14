#!/bin/bash
echo "platform|backend|benchmark|time" > benchmark.md
echo "--------|-------|---------|----" >> benchmark.md
for i in {2..6}
do
    export GOLESS_BACKEND=stackless
    . $PYPY_VENV/bin/activate
    /usr/bin/time --format="%es" pypy ../ga_client.py -i --requests $i --iterations $i |& tail -fn1 | xargs echo "pypy|$GOLESS_BACKEND|$i requests $i iterations|" >> benchmark.md
    deactivate
    . $CPYTHON_VENV/bin/activate
    /usr/bin/time --format="%es" python ../ga_client.py -i --requests $i --iterations $i |& tail -fn1 | xargs echo "python|$GOLESS_BACKEND|$i requests $i iterations|" >> benchmark.md
    deactivate
    . $PYPY_VENV/bin/activate
    /usr/bin/time --format="%es" python3 ../ga_client.py -i --requests $i --iterations $i |& tail -fn1 | xargs echo "python3|$GOLESS_BACKEND|$i requests $i iterations|" >> benchmark.md
    deactivate

    export GOLESS_BACKEND=gevent
    . $PYPY_VENV/bin/activate
    /usr/bin/time --format="%es" pypy ../ga_client.py -i --requests $i --iterations $i |& tail -fn1 | xargs echo "pypy|$GOLESS_BACKEND|$i requests $i iterations|" >> benchmark.md
    deactivate
    . $CPYTHON_VENV/bin/activate
    /usr/bin/time --format="%es" python ../ga_client.py -i --requests $i --iterations $i |& tail -fn1 | xargs echo "python|$GOLESS_BACKEND|$i requests $i iterations|" >> benchmark.md
    deactivate
    . $PYPY_VENV/bin/activate
    /usr/bin/time --format="%es" python3 ../ga_client.py -i --requests $i --iterations $i |& tail -fn1 | xargs echo "python3|$GOLESS_BACKEND|$i requests $i iterations|" >> benchmark.md
    deactivate
done
