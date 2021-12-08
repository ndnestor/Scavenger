import QtQuick
import QtQuick.Controls

Rectangle {
    property string title
    property string preview
    property string token

    color: "black"
    width: window.width
    height: 40
    anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined
    anchors.top: parent ? parent.bottom : undefined
    anchors.topMargin: 2

    Button {
        anchors.fill: parent
        background: Rectangle {
            anchors.fill: parent
            color: "#000000"
        }
        onClicked: {
            print("Clicked on a card")
            window.resultViewer.show(token)
        }

        Text {
            text: qsTr(title);
            anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined
            anchors.top: parent ? parent.top : undefined
            anchors.topMargin: 5
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
            font.pointSize: 10
        }

        Text {
            textFormat: Text.RichText
            text: qsTr(preview)
            anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined
            anchors.bottom: parent ? parent.bottom : undefined
            anchors.bottomMargin: 5
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
            font.pointSize: 10
        }
    }
}