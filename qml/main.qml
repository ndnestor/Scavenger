import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import Searcher 1.0

ApplicationWindow {
    id: window
    width: 400
    height: 500
    visible: true
    title: qsTr("Scavenger")

    Material.theme: Material.Dark
    Material.accent: Material.LightBlue

    TextField {
        id: searchField
        width: 300
        text: qsTr("")
        selectByMouse: true
        placeholderText: qsTr("Search with Scavenger")
        verticalAlignment: Text.AlignVCenter
        anchors.horizontalCenter: parent.horizontalCenter
        //anchors.top: image.bottom
        anchors.topMargin: 60
    }

    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: {
            searcher.query = searchField.text
        }
    }

    Searcher {
        id: searcher
    }
}
