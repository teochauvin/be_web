
// Tokens
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyODliMGRmYS0xZDNmLTRhM2UtYjdmNS1iNjhjZTdhZGI1ZGIiLCJpZCI6OTA2MzYsImlhdCI6MTY1MDU0NjcxMH0.juEG9AbeeY3WwnDisZ-009glQo8cRdfmZM4LO1wCcII';

//////////////////////////////////
//////// APP JSS A REECRIRE PLUS PROPREMENT JE VOUS EN CONJUREEEEE
////////////////////////////////

const viewer = new Cesium.Viewer('cesiumContainer', {
    // creation du terrain 
    terrainProvider: Cesium.createWorldTerrain(),  
});

viewer.scene.globe.enableLighting = true;
viewer.scene.globe.nightFadeInDistance = 0;

const scene = viewer.scene;

//// POUR QUE LA TERRE TOURNE
var inertialToFixed = new Cesium.Matrix3();

function updateCameraInertial(viewer) {
    const camera = viewer.camera

    /// on applique pas les transformation dans ces cas la 
    if (viewer.scene.mode !== Cesium.SceneMode.SCENE3D || Cesium.defined(viewer.trackedObject)) {
        return;
    }

    /// si la matrice de passage n'est pas définie 
    if (!Cesium.defined(Cesium.Transforms.computeIcrfToFixedMatrix(viewer.clock.currentTime, inertialToFixed))) {
        Cesium.Transforms.computeTemeToPseudoFixedMatrix(viewer.clock.currentTime, inertialToFixed);
    }

    // on calcule la transformation à appliquer à la camera et offset est sa nouvelle position (ou une copie)
    const transform = Cesium.Matrix4.fromRotationTranslation(inertialToFixed, Cesium.Cartesian3.ZERO, viewer.scene.camera.transform);
    const offset = Cesium.Matrix4.multiplyByPoint(camera.transform, camera.position, new Cesium.Cartesian3());

    const inverseTransform = Cesium.Matrix4.inverseTransformation(transform, new Cesium.Matrix4());
    Cesium.Matrix4.multiplyByPoint(inverseTransform, offset, offset);
    
    camera.lookAtTransform(transform, offset);
}

// callback 
viewer.clock.onTick.addEventListener(function() {
    updateCameraInertial(viewer);
});


// on recupere les variables utiles
const satellites = JSON.parse(JSON.stringify(data.satellites_infos))


// La simulation se déroulera en x1 
viewer.clock.multiplier = 1;

// La simulation commence quand la page s'ouvre
viewer.clock.shouldAnimate = true;

// liste des entites satellite
const satEntity_list = [];
const positionProperty_list = [];


for (let j = 0; j < satellites.length; j++){

    // La position et le timestamp sont sauvegardés ensemble pour pouvoir animer le point (trajectoire)
    const positionProperty = new Cesium.SampledPositionProperty();

    // time variables are the same for all sats (V1)
    const timeSep = satellites[j].timeSep;
    const nPoints =  satellites[j].npoints

    // on recupere le temps total du calcul de trajectoire
    const totalSeconds = timeSep * nPoints;

    // le debut et la fin de la simulation 
    const start = Cesium.JulianDate.fromIso8601(satellites[j].timeStart);
    const stop = Cesium.JulianDate.addSeconds(start, totalSeconds, new Cesium.JulianDate());

    // gestion de l'horloge (start et stop sont des objets Date en javascript, d'ou le clone())
    viewer.clock.startTime = start.clone();
    viewer.clock.stopTime = stop.clone();

    viewer.clock.currentTime = start.clone();
    viewer.timeline.zoomTo(start, stop);


    for (let i = 0; i < nPoints; i++) {
        const dataPoint = satellites[j].angularPosition[i]

        // Declare the time for this individual sample and store it in a new JulianDate instance.
        const time = Cesium.JulianDate.addSeconds(start, i * timeSep, new Cesium.JulianDate());
        const position = Cesium.Cartesian3.fromDegrees(dataPoint.longitude, dataPoint.latitude, dataPoint.height);

        // Store the position along with its timestamp.
        // Here we add the positions all upfront, but these can be added at run-time as samples are received from a server.
        positionProperty.addSample(time, position);

        viewer.entities.add({
            description: `Location: (${dataPoint.longitude}, ${dataPoint.latitude}, ${dataPoint.height})`,
            position: position,
        });

    }

    // permet d'interpoler la trajectoire entre les differents points de calculs. Ici on utilise une interpolation
    // Lagrange, les trajectoires sont convexes alors le degre 3 est largement suffisant 

    positionProperty.setInterpolationOptions({
        interpolationDegree : 3,
        interpolationAlgorithm : Cesium.LagrangePolynomialApproximation
    });

    // on ajoute à la liste
    positionProperty_list.push(positionProperty)

    // Create an entity to both visualize the entire radar sample series with a line and add a point that moves along the samples.
    const satEntity = viewer.entities.add({
        availability: new Cesium.TimeIntervalCollection([ new Cesium.TimeInterval({ start: start, stop: stop }) ]),
        position: positionProperty,
        point: { pixelSize: 3, color: Cesium.Color.GREEN },
        label: { id : 'satellite ' + j , 
        text: satellites[j].nameSate,
        horizontalOrigin: Cesium.HorizontalOrigin.LEFT, 
        font:'8px sans-serif',
        showBackground: true,
        translucencyByDistance : new Cesium.NearFarScalar(5.0e7, 1.0, 1.0e8, 0.0)}
    });

    // on ajoute à la liste 
    satEntity_list.push(satEntity)
}




// Make the camera track this moving entity.

