function onLoad() {
    let gitlabButton = document.getElementById("gitlab_button")
    console.log(gitlabButton)
    gitlabButton.onclick = function() {
        window.open("https://gitlab.com/TommasoBarberis/diversite-phylogenetique-de-l-assiette-au-jardin");
    }

    let ucblButton = document.getElementById("ucbl_button");
    ucblButton.onclick = function() {
        window.open("https://www.univ-lyon1.fr/");
    }

    let marmitonButton = document.getElementById("marmiton_button");
    marmitonButton.onclick = function() {
        window.open("https://www.marmiton.org/");
    }
}