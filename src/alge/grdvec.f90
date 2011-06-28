!-------------------------------------------------------------------------------

!     This file is part of the Code_Saturne Kernel, element of the
!     Code_Saturne CFD tool.

!     Copyright (C) 1998-2011 EDF S.A., France

!     contact: saturne-support@edf.fr

!     The Code_Saturne Kernel is free software; you can redistribute it
!     and/or modify it under the terms of the GNU General Public License
!     as published by the Free Software Foundation; either version 2 of
!     the License, or (at your option) any later version.

!     The Code_Saturne Kernel is distributed in the hope that it will be
!     useful, but WITHOUT ANY WARRANTY; without even the implied warranty
!     of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!     GNU General Public License for more details.

!     You should have received a copy of the GNU General Public License
!     along with the Code_Saturne Kernel; if not, write to the
!     Free Software Foundation, Inc.,
!     51 Franklin St, Fifth Floor,
!     Boston, MA  02110-1301  USA

!-------------------------------------------------------------------------------

subroutine grdvec &
!================

 ( ivar   , imrgra , inc    , iccocg , nswrgp , imligp ,          &
   iwarnp , nfecra , epsrgp , climgp , extrap ,                   &
   vel    , ilved  , coefav , coefbv ,                            &
   gradv )

!===============================================================================
! FONCTION :
! ----------

! APPEL DES DIFFERENTES ROUTINES DE CALCUL DE GRADIENT CELLULE

!-------------------------------------------------------------------------------
! Arguments
!__________________.____._____.________________________________________________.
! name             !type!mode ! role                                           !
!__________________!____!_____!________________________________________________!
! ivar             ! e  ! <-- ! numero de la variable                          !
!                  !    !     !   destine a etre utilise pour la               !
!                  !    !     !   periodicite uniquement (pering)              !
!                  !    !     !   on pourra donner ivar=0 si la                !
!                  !    !     !   variable n'est ni une composante de          !
!                  !    !     !   la vitesse, ni une composante du             !
!                  !    !     !   tenseur des contraintes rij                  !
! imrgra           ! e  ! <-- ! methode de reconstruction du gradient          !
!                  !    !     !  0 reconstruction 97                           !
!                  !    !     !  1 moindres carres                             !
!                  !    !     !  2 moindres carres support etendu              !
!                  !    !     !    complet                                     !
!                  !    !     !  3 moindres carres avec selection du           !
!                  !    !     !    support etendu                              !
! inc              ! e  ! <-- ! indicateur = 0 resol sur increment             !
!                  !    !     !              1 sinon                           !
! iccocg           ! e  ! <-- ! indicateur = 1 pour recalcul de cocg           !
!                  !    !     !              0 sinon                           !
! nswrgp           ! e  ! <-- ! nombre de sweep pour reconstruction            !
!                  !    !     !             des gradients                      !
! imligp           ! e  ! <-- ! methode de limitation du gradient              !
!                  !    !     !  < 0 pas de limitation                         !
!                  !    !     !  = 0 a partir des gradients voisins            !
!                  !    !     !  = 1 a partir du gradient moyen                !
! iwarnp           ! i  ! <-- ! verbosity                                      !
! nfecra           ! e  ! <-- ! unite du fichier sortie std                    !
! epsrgp           ! r  ! <-- ! precision relative pour la                     !
!                  !    !     !  reconstruction des gradients 97               !
! climgp           ! r  ! <-- ! coef gradient*distance/ecart                   !
! extrap           ! r  ! <-- ! coef extrap gradient                           !
! vel(3,ncelet)    ! tr ! <-- ! variable (vitesse)                             !
! coefav,coefbv    ! tr ! <-- ! tableaux des cond lim pour pvar                !
!   (3,nfabor)     !    !     !  sur la normale a la face de bord              !
! gradv          ! tr ! --> ! gradient de vitesse                            !
!   (3,3,ncelet)   !    !     !                                                !
!__________________!____!_____!________________________________________________!

!     TYPE : E (ENTIER), R (REEL), A (ALPHANUMERIQUE), T (TABLEAU)
!            L (LOGIQUE)   .. ET TYPES COMPOSES (EX : TR TABLEAU REEL)
!     MODE : <-- donnee, --> resultat, <-> Donnee modifiee
!            --- tableau de travail
!===============================================================================

!===============================================================================
! Module files
!===============================================================================

use paramx
use pointe
use parall
use period
use mesh
use cstphy
use cstnum
use albase
use cplsat
use dimens, only: ndimfb

!===============================================================================

implicit none

! Arguments

integer          ivar   , imrgra , inc    , iccocg , nswrgp
integer          imligp ,iwarnp  , nfecra
double precision epsrgp , climgp , extrap

double precision vel(3*ncelet)
double precision coefav(*), coefbv(*)
double precision gradv(3*3*ncelet)

logical ilved

! Local variables

integer          iel, isou, jsou

double precision, dimension(:,:), allocatable :: veli
double precision, dimension(:,:,:), allocatable :: gradvi

!===============================================================================

!===============================================================================
! 1. COMPUTATION OF THE GARDIENT
!===============================================================================

! the velocity and the gradient fields are interleaved
if (ilved) then

  call cgdvec                                                     &
  !==========
 ( ncelet , ncel   , nfac   , nfabor , ivar   ,                   &
   imrgra , inc    , nswrgp ,                                     &
   iwarnp , nfecra , imligp , epsrgp , extrap , climgp ,          &
   ifacel , ifabor , isympa ,                                     &
   volume , surfac , surfbo , surfbn , pond   ,                   &
   dist   , distb  , dijpf  , diipb  , dofij  ,                   &
   xyzcen , cdgfac , cdgfbo , coefav , coefbv , vel    ,          &
   cocgu  ,                                                       &
   gradv  )

! We interleave the velocity
else

  !Allocation
  allocate(veli(3,ncelet))
  allocate(gradvi(3,3,ncelet))

  do isou = 1, 3
    do iel = 1, ncelet
      veli(isou,iel) = vel(iel + (isou-1)*ncelet)
    enddo
  enddo

  call cgdvec                                                     &
  !==========
 ( ncelet , ncel   , nfac   , nfabor , ivar   ,                   &
   imrgra , inc    , nswrgp ,                                     &
   iwarnp , nfecra , imligp , epsrgp , extrap , climgp ,          &
   ifacel , ifabor , isympa ,                                     &
   volume , surfac , surfbo , surfbn , pond   ,                   &
   dist   , distb  , dijpf  , diipb  , dofij  ,                   &
   xyzcen , cdgfac , cdgfbo , coefav , coefbv , veli   ,          &
   cocgu  ,                                                       &
   gradvi )


  do isou = 1, 3
    do jsou = 1, 3
      do iel = 1, ncelet
        gradv(iel + (jsou-1)*ncelet + (isou-1)*3*ncelet) = gradvi(isou,jsou,iel)
      enddo
    enddo
  enddo

  ! Free memory
  deallocate(veli, gradvi)

endif

return
end subroutine
