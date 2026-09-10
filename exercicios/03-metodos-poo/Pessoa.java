// Pessoa.java — 10 setembro 2026, 02:42
public class Pessoa{
	private String nome;
	private String genero;
	private int idade;
	
	public Pessoa(String nome, String genero, int idade){
		this.nome = nome;
		this.genero = genero;
		this.idade = idade;
	}
	
	public boolean maiorDeIdade(){
        	return idade >= 18;
	}
	
	public String descricao(){
    	    	String estado;
		String artigo;
	
       		if(maiorDeIdade()){
               		estado = "é maior de idade.";
        	}
        	else{
                	estado = "é menor de idade.";
        	}

		if (genero.equals("M")){
			artigo = "O";
		}
		else{
			artigo  = "A";
		}
		
		return artigo + " " + nome + " tem " + idade + " anos e " + estado;
	}

	public void setIdade(int idade){
		if(idade < 0){
			System.out.println("(Atenção: A tentativa de mudança de idade '" + idade + "' para " + nome + " não pode ser negativa.)");
		}
		else{
			this.idade = idade;
		}
	}
}



