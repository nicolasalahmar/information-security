# Core
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID


class DigitalCertificate:

    @staticmethod
    def generateCSR(name, private_key):
        # Create a CSR
        csr = x509.CertificateSigningRequestBuilder()

        # add subject to the csr
        csr = csr.subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, name),
        ]))

        # add public key
        csr = csr.add_extension(
            x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
            critical=False
        )

        # sign the csr with private key
        csr = csr.sign(
            private_key, hashes.SHA256(), default_backend()
        )

        return csr

    @staticmethod
    def generateDigitalCertificate(csr, private_key):
        # Generate the CA certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'SERVER'),
            x509.NameAttribute(NameOID.COMMON_NAME, 'My SERVER'),
        ])

        ca_cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
            private_key.public_key()
        ).serial_number(x509.random_serial_number()).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True
        ).sign(private_key, hashes.SHA256())

        # Sign the CSR with the CA private key and certificate
        signed_cert = x509.CertificateBuilder().subject_name(
            csr.subject
        ).issuer_name(
            ca_cert.subject
        ).public_key(
            csr.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).sign(private_key, hashes.SHA256())

        return signed_cert
