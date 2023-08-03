<?php
//Check password
if(!isset($_POST['password'])){
	echo "This specific page is admin's page.";
	return;
}
$password = $_POST['password'] ?? '';
$password = hash('sha256', $password);
$passhash = file_get_contents('passhash.key');
if($password != $passhash){
    echo 'Wrong Password!!!';
	return;
}


//Custom Dimperpreter
class Dimperpreter {
    var $code;		//source
	var $i=0;		//main index
	var $l=0;		//source length
    //custom vars
    var $lastStart=0;
    var $lastEnd=0;
	public function __construct(string $x){
		$x = ' ' . $x;
		$this->code = $x;
		$this->l = strlen($x);
	}
	public function Next(){
        $this->lastStart = $this->i;
        //
		$o = $this->i;	//index 2
		$c = '';		//char at index2
		$arg = '';		//last readed argument;
		$args = (array) null;
		while($o<$this->l){
			$c=$this->code[$o];
			if($c=='@') $o++;
			else if($c==',' || $c==';'){
				$arg=substr($this->code,$this->i,$o-$this->i);
				$this->i=$o + 1;
				$o++;
				$arg=str_replace("@@","@",$arg);
				$arg=str_replace("@,",",",$arg);
				$arg=str_replace("@;",";",$arg);
				array_push($args,$arg);
				if($c==';'){
                    //
                    $this->lastEnd = $o;
					//
                    return $args;
                }
			}
			$o++;
		}
		$this->i=$o;
		return null;
	}
    public function ReadRawBeforeLast(){
        return substr($this->code,0,$this->lastStart);
    }
    public function ReadRawInsideLast(){
        return substr($this->code,$this->lastStart,$this->lastEnd - $this->lastStart);
    }
    public function ReadRawAfterLast(){
        return substr($this->code,$this->lastStart);
    }
}

echo shell_exec("python calc_hashes.py");

$dimp = new Dimperpreter(file_get_contents('hashes.dim'));
$line = $dimp->Next();
while($line){
    print_r($line);
    echo '<br>';
    $line = $dimp->Next();
}