if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
else
  python generate.py "$@"
fi