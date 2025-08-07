resource "kubernetes_deployment_v1" "mailhog" {
  metadata {
    name      = "mailhog"
    namespace = kubernetes_namespace_v1.chat.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = { app = "mailhog" }
    }

    template {
      metadata {
        labels = { app = "mailhog" }
      }

      spec {
        container {
          name  = "mailhog"
          image = "mailhog/mailhog:v1.0.1"

          port {
            name           = "smtp"
            container_port = 1025
          }
          port {
            name           = "http"
            container_port = 8025
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "mailhog_smtp" {
  metadata {
    name      = "mailhog-smtp"
    namespace = kubernetes_namespace_v1.chat.metadata[0].name
  }

  spec {
    selector = { app = "mailhog" }

    port {
      name        = "smtp"
      port        = 1025
      target_port = "smtp"
    }

    type = "ClusterIP"
  }
}

resource "kubernetes_service_v1" "mailhog_web" {
  metadata {
    name      = "mailhog-web"
    namespace = kubernetes_namespace_v1.chat.metadata[0].name
  }

  spec {
    selector = { app = "mailhog" }

    port {
      name        = "http"
      port        = 8025
      target_port = "http"
      # node_port = 30025   # optional fixed NodePort
    }

    type = "NodePort"
  }
}
