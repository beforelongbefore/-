curdir=`pwd`
cd app/simulation/export3
java -cp com.xj.anylogic.engine.jar:com.xj.anylogic.engine.nl.jar:model.jar:com.xj.anylogic.engine.sa.jar -Xmx64m running_model_outside.MyApplication
cd $curdir
python3 app/simulation/aftersim.py $1