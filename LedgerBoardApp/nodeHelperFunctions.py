from LedgerBoardApp.models import Node



def newNode(host, version):
    feedback = ""

    if Node.objects.filter(host = host).exists():
        feedback = "Host already exists."

        return feedback #basically say it exist already

    node = Node(host = host, version=version, secondsSinceLastInteraction=0)
    node.save()
    return feedback
