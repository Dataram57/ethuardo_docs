window.onload = () => {
    //Init responsivness
    InitResponsive();
    //Navigate to the currently opened document
    ExplorerNavigate();
    //Update content-path
    UpdateContentPath();
    //Generate sections of the document
    RenderSections();
};

/*
================================================
|                                              |
|                 Responsivity                 |
|                                              |
================================================
*/

const screen_sizes = [0, 576, 768, 992, 1200];
const screen_sizes_names = ['xs', 'sm', 'md', 'lg', 'xl'];
let screen_lastState = -1;
let repsonsive_screen = null;

const UpdateScreenSize = () => {
    const oldState = screen_lastState;
    const w = document.body.clientWidth;
    let i = screen_sizes.length;
    while(--i > -1)
        if(w >= screen_sizes[i])
            break;
    if(screen_lastState != i){
        screen_lastState = i;
        //update responsive-screen
        if(repsonsive_screen){
            i = repsonsive_screen.length;
            while(--i > -1){
                //remove old class
                if(oldState != -1)
                    repsonsive_screen[i].classList.remove('screen-' + screen_sizes_names[oldState]);
                //add new class
                repsonsive_screen[i].classList.add('screen-' + screen_sizes_names[screen_lastState]);
            }
        }
    }    
};

const InitResponsive = () => {
    repsonsive_screen = document.getElementsByClassName('responsive-screen');
    if(repsonsive_screen.length == 0)
        repsonsive_screen = null;
    const e = () => {
        UpdateScreenSize();
    };
    window.addEventListener("resize", e);
    e();
};

/*
================================================
|                                              |
|                 Mobile Burger                |
|                                              |
================================================
*/

const MobileBurgerClick = () => {
    const mobileNavbar = document.getElementById('mobile-navbar');
    const panelLeft = document.getElementById('panel-left');
    const panelMiddle = document.getElementById('panel-middle');
    if(mobileNavbar.classList.contains('mobile')){
        panelLeft.classList.remove('mobile');
        mobileNavbar.classList.remove('mobile');
        panelMiddle.classList.remove('mobile');
    }else{
        panelLeft.classList.add('mobile');
        mobileNavbar.classList.add('mobile');
        panelMiddle.classList.add('mobile');
    }
};

/*
================================================
|                                              |
|                   Explorer                   |
|                                              |
================================================
*/

const ToggleFolder = (header) => {
    header = header.parentNode;
    //css
    header.classList.toggle('folder-opened');
    //hide/show
    header = header.lastElementChild;
    header.hidden = !header.hidden;
};

const ExplorerNavigate = (url) => {
    if(!url)
        url = window.location.pathname;
    console.log(url);
};

/*
================================================
|                                              |
|                 Content-Path                 |
|                                              |
================================================
*/

const UpdateContentPath = (url) => {
    if(!url)
        url = window.location.pathname;
    console.log(url);
};

/*
================================================
|                                              |
|                   Sections                   |
|                                              |
================================================
*/

const renderSectionClassNames = {
    h1: 'section-h1'
    ,h2: 'section-h2'
    ,h3: 'section-h3'
};
const sectionSymbolsToReplace = [
    [' ', '-']
    ,["\n", '-']
];

const ToSectionName = (text) => {
    text = text.toLowerCase();
    while(text.length != (text = text.trim()).length);
    let i = sectionSymbolsToReplace.length;
    while(--i > -1)
        text = text.replaceAll(sectionSymbolsToReplace[i][0],sectionSymbolsToReplace[i][1]);
    return text;
};

const RenderSections = () => {
    const tag = document.getElementById('content-navigation');
    const children = document.getElementById('content').children;
    const usedSectionNames = {};
    let f = 0;
    let sectionName = '';
    let lastSectionIndex = 1;
    let className = '';
    let section = null
    for(let i = 0; i < children.length; i++){
        className = renderSectionClassNames[children[i].tagName.toLowerCase()];
        if(className){
            section = document.createElement("a");
            section.classList.add('section');
            
            //create a correct unique and systematic section name
            sectionName = ToSectionName(children[i].textContent)
            if(usedSectionNames[sectionName] !== undefined)
                lastSectionIndex = ++usedSectionNames[sectionName];
            else{
                lastSectionIndex = 1;
                usedSectionNames[sectionName] = lastSectionIndex;
            }
            //convert to usable
            if(lastSectionIndex > 1)
                sectionName += '_' + lastSectionIndex.toString();

            //assign this name
            section.setAttribute('name', sectionName)
            children[i].appendChild(section);
            tag.innerHTML += '<li class="' + className + '"><a href="#' + sectionName + '">' + children[i].textContent + '</a></li>';
        }
    }
};