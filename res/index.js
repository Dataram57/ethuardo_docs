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

const ScanAllElementsInside = (element, func_element) => {
    const tree = [element];
    let i = 0;
    while(i >= 0){
        //check
        if(func_element(tree[i]))
            return;
        //in
        if(tree[i].firstElementChild)
            tree.push(tree[i++].firstElementChild);
        else
            while(i >= 0){
                //next
                tree[i] = tree[i].nextElementSibling;
                if(tree[i])
                    break;
                else{
                    tree.pop();
                    i--;
                }
            }
    }
};

const ExplorerNavigate = (path) => {
    if(!path)
        path = window.location.pathname;
    const mainParent = document.getElementById('explorer').firstElementChild;
    let href = '';
    ScanAllElementsInside(mainParent, element => {
        href = element.getAttribute('href');
        if(href)
            if(href == path){
                //found element with this path
                element = element.parentElement;
                element.classList.add('visit')
                while(element != mainParent){
                    element = element.parentElement;
                    if(element.firstElementChild)
                        if(element.firstElementChild.classList.contains('folder'))
                            element.firstElementChild.click();
                }
                //end scanning
                return true;
            }
    });
};

/*
================================================
|                                              |
|                 Content-Path                 |
|                                              |
================================================
*/

const UpdateContentPath = (path) => {
    const tag = document.getElementById('content-path');
    if(!path)
        path = window.location.pathname;
    const routes = path.split('/');
    let length = 0;
    for(let i = 0; i < routes.length; i++){
        if(routes[i].length > 0){
            tag.innerHTML += ((length > 0) ? '&gt;' : '') + '<a href="' + path.substring(0, (length += routes[i].length + 1)) + '">' + routes[i] + '</a>';
        }
    }
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